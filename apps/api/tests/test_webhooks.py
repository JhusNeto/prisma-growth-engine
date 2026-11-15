from uuid import UUID, uuid4

import pytest
from app.commerce_models import Order, ProviderEvent
from app.config import Settings, get_settings
from app.db import get_engine, get_session
from app.main import app
from app.models import OutboxEvent
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

TEST_HOTTOK = "test-hottok-secret-123"


@pytest.fixture
def webhook_client():
    with get_engine().connect() as connection:
        transaction = connection.begin()
        session = Session(
            bind=connection,
            join_transaction_mode="create_savepoint",
        )

        app.dependency_overrides[get_session] = lambda: session
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


def build_payload(
    event_id: str | None = None,
    transaction_id: str | None = None,
    event: str = "PURCHASE_APPROVED",
    amount: float = 29.90,
) -> dict:
    return {
        "id": event_id or f"evt-{uuid4().hex}",
        "creation_date": 1794780000000,
        "event": event,
        "version": "2.0.0",
        "data": {
            "product": {"id": 999999, "name": "Precifica Fácil"},
            "buyer": {
                "name": "Comprador Teste PII",
                "email": "cliente@example.com",
                "document": "00000000000",
            },
            "purchase": {
                "transaction": transaction_id or f"HP{uuid4().hex[:14].upper()}",
                "status": "APPROVED" if event == "PURCHASE_APPROVED" else "REFUNDED",
                "price": {"value": amount, "currency_value": "BRL"},
                "approved_date": 1794780010000,
            },
        },
    }


def test_webhook_rejects_invalid_token(webhook_client):
    client, _ = webhook_client
    response = client.post(
        "/v1/webhooks/hotmart",
        headers={"X-Hotmart-Hottok": "wrong-token"},
        json=build_payload(),
    )
    assert response.status_code == 401


def test_webhook_processes_approved_purchase_and_strips_pii(webhook_client):
    client, session = webhook_client
    payload = build_payload()

    response = client.post(
        "/v1/webhooks/hotmart",
        headers={"X-Hotmart-Hottok": TEST_HOTTOK},
        json=payload,
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "processed"
    assert body["order_status"] == "approved"

    order = session.get(Order, UUID(body["order_id"]))
    assert order is not None
    assert order.amount_cents == 2990
    assert order.status == "approved"

    stored_event = session.scalar(
        select(ProviderEvent).where(ProviderEvent.event_id == payload["id"])
    )
    assert stored_event is not None
    assert stored_event.processed_at is not None
    assert "buyer" not in stored_event.payload

    outbox = session.scalar(
        select(OutboxEvent).where(
            OutboxEvent.aggregate_id == order.id,
            OutboxEvent.event_type == "order.approved",
        )
    )
    assert outbox is not None
    assert outbox.payload["amount_cents"] == 2990


def test_webhook_is_idempotent_on_duplicate_event(webhook_client):
    client, session = webhook_client
    payload = build_payload()

    first = client.post(
        "/v1/webhooks/hotmart",
        headers={"X-Hotmart-Hottok": TEST_HOTTOK},
        json=payload,
    )
    assert first.status_code == 200
    assert first.json()["status"] == "processed"

    second = client.post(
        "/v1/webhooks/hotmart",
        headers={"X-Hotmart-Hottok": TEST_HOTTOK},
        json=payload,
    )
    assert second.status_code == 200
    assert second.json()["status"] == "duplicate"

    order_count = session.scalar(
        select(func.count(Order.id)).where(
            Order.provider_transaction_id == payload["data"]["purchase"]["transaction"]
        )
    )
    assert order_count == 1


def test_webhook_updates_order_on_refund(webhook_client):
    client, session = webhook_client
    tx_id = f"HP{uuid4().hex[:14].upper()}"

    approved = client.post(
        "/v1/webhooks/hotmart",
        headers={"X-Hotmart-Hottok": TEST_HOTTOK},
        json=build_payload(transaction_id=tx_id, event="PURCHASE_APPROVED"),
    )
    assert approved.status_code == 200
    order_id = UUID(approved.json()["order_id"])

    refunded = client.post(
        "/v1/webhooks/hotmart",
        headers={"X-Hotmart-Hottok": TEST_HOTTOK},
        json=build_payload(transaction_id=tx_id, event="PURCHASE_REFUNDED"),
    )
    assert refunded.status_code == 200
    assert refunded.json()["order_status"] == "refunded"

    order = session.get(Order, order_id)
    assert order is not None
    assert order.status == "refunded"

    events = list(
        session.scalars(
            select(OutboxEvent.event_type).where(OutboxEvent.aggregate_id == order_id)
        ).all()
    )
    assert events == ["order.approved", "order.refunded"]
