from uuid import uuid4

import pytest
from app.config import Settings, get_settings
from app.db import get_engine, get_session
from app.main import app
from app.security import require_admin
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

TEST_HOTTOK = "test-hottok-analytics-123"


@pytest.fixture
def analytics_client():
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


def send_webhook(client: TestClient, event: str, amount: float, tx_id: str | None = None):
    response = client.post(
        "/v1/webhooks/hotmart",
        headers={"X-Hotmart-Hottok": TEST_HOTTOK},
        json={
            "id": f"evt-{uuid4().hex}",
            "creation_date": 1794790000000,
            "event": event,
            "version": "2.0.0",
            "data": {
                "product": {"id": 999999, "name": "Precifica Fácil"},
                "purchase": {
                    "transaction": tx_id or f"HP{uuid4().hex[:14].upper()}",
                    "status": "APPROVED",
                    "price": {"value": amount, "currency_value": "BRL"},
                    "approved_date": 1794790010000,
                },
            },
        },
    )
    assert response.status_code == 200
    return response.json()


def test_orders_and_analytics_require_authentication():
    with TestClient(app) as client:
        assert client.get("/v1/orders").status_code == 401
        assert client.get("/v1/analytics/overview").status_code == 401


def test_orders_listing_and_overview_metrics(analytics_client):
    client, _ = analytics_client

    baseline = client.get("/v1/analytics/overview").json()

    tx1 = f"HP{uuid4().hex[:14].upper()}"
    tx2 = f"HP{uuid4().hex[:14].upper()}"

    send_webhook(client, "PURCHASE_APPROVED", 29.90, tx_id=tx1)
    send_webhook(client, "PURCHASE_APPROVED", 39.90, tx_id=tx2)
    send_webhook(client, "PURCHASE_REFUNDED", 39.90, tx_id=tx2)

    approved_orders = client.get("/v1/orders", params={"status": "approved"}).json()
    assert any(o["provider_transaction_id"] == tx1 for o in approved_orders)
    assert all(o["status"] == "approved" for o in approved_orders)

    refunded_orders = client.get("/v1/orders", params={"status": "refunded"}).json()
    assert any(o["provider_transaction_id"] == tx2 for o in refunded_orders)

    overview = client.get("/v1/analytics/overview").json()
    assert overview["approved_orders"] == baseline["approved_orders"] + 1
    assert overview["refunded_orders"] == baseline["refunded_orders"] + 1
    assert overview["gross_approved_cents"] == baseline["gross_approved_cents"] + 2990
    assert overview["reversed_cents"] == baseline["reversed_cents"] + 3990
    assert overview["net_revenue_cents"] == baseline["net_revenue_cents"] + 2990 - 3990
    assert overview["pending_outbox_events"] >= baseline["pending_outbox_events"] + 3
