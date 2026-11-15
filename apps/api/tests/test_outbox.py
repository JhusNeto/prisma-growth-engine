from uuid import UUID, uuid4

import pytest
from app.config import Settings, get_settings
from app.db import get_engine, get_session
from app.main import app
from app.security import require_admin
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

TEST_HOTTOK = "test-hottok-outbox-123"


@pytest.fixture
def outbox_client():
    with get_engine().connect() as connection:
        transaction = connection.begin()
        session = Session(
            bind=connection,
            join_transaction_mode="create_savepoint",
        )

        app.dependency_overrides[get_session] = lambda: session
        app.dependency_overrides[require_admin] = lambda: None
        app.dependency_overrides[get_settings] = lambda: Settings(
            database_url="postgresql+psycopg://unused",
            admin_api_key="unused",
            hotmart_hottok=TEST_HOTTOK,
        )

        try:
            with TestClient(app) as client:
                yield client, session
        finally:
            app.dependency_overrides.clear()
            session.close()
            transaction.rollback()


def trigger_approved_sale(client: TestClient) -> str:
    response = client.post(
        "/v1/webhooks/hotmart",
        headers={"X-Hotmart-Hottok": TEST_HOTTOK},
        json={
            "id": f"evt-{uuid4().hex}",
            "creation_date": 1794785000000,
            "event": "PURCHASE_APPROVED",
            "version": "2.0.0",
            "data": {
                "product": {"id": 999999, "name": "Precifica Fácil"},
                "purchase": {
                    "transaction": f"HP{uuid4().hex[:14].upper()}",
                    "status": "APPROVED",
                    "price": {"value": 29.90, "currency_value": "BRL"},
                    "approved_date": 1794785010000,
                },
            },
        },
    )
    assert response.status_code == 200
    return response.json()["order_id"]


def test_outbox_requires_admin_key():
    with TestClient(app) as client:
        response = client.get("/v1/outbox/pending")
    assert response.status_code == 401


def test_list_pending_and_acknowledge_idempotently(outbox_client):
    client, _ = outbox_client
    order_id = trigger_approved_sale(client)

    pending = client.get("/v1/outbox/pending", params={"event_type": "order.approved"})
    assert pending.status_code == 200
    events = pending.json()

    matched = [e for e in events if e["aggregate_id"] == order_id]
    assert len(matched) == 1
    event_id = matched[0]["id"]
    assert matched[0]["published_at"] is None

    ack_first = client.post(f"/v1/outbox/{event_id}/ack")
    assert ack_first.status_code == 200
    body_first = ack_first.json()
    assert body_first["status"] == "acknowledged"
    published_at = body_first["event"]["published_at"]
    assert published_at is not None

    # Evento confirmado não deve mais aparecer nos pendentes
    pending_after = client.get("/v1/outbox/pending", params={"event_type": "order.approved"})
    assert all(e["id"] != event_id for e in pending_after.json())

    # Segundo ack deve ser idempotente e manter o timestamp original
    ack_second = client.post(f"/v1/outbox/{event_id}/ack")
    assert ack_second.status_code == 200
    body_second = ack_second.json()
    assert body_second["status"] == "already_acknowledged"
    assert body_second["event"]["published_at"] == published_at


def test_acknowledge_unknown_event_returns_404(outbox_client):
    client, _ = outbox_client
    response = client.post(f"/v1/outbox/{UUID(int=0)}/ack")
    assert response.status_code == 404
