from uuid import uuid4

import pytest
from app.db import get_engine, get_session
from app.main import app
from app.models import OutboxEvent
from app.security import require_admin
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session


@pytest.fixture
def db_client():
    with get_engine().connect() as connection:
        transaction = connection.begin()
        session = Session(
            bind=connection,
            join_transaction_mode="create_savepoint",
        )

        app.dependency_overrides[get_session] = lambda: session
        app.dependency_overrides[require_admin] = lambda: None

        try:
            with TestClient(app) as client:
                yield client, session
        finally:
            app.dependency_overrides.clear()
            session.close()
            transaction.rollback()


def create_product(client):
    response = client.post(
        "/v1/products",
        json={
            "slug": f"teste-{uuid4().hex[:12]}",
            "name": "Produto para ofertas",
            "audience": "Empreendedores",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()["id"]


def test_create_offer_and_outbox(db_client):
    client, session = db_client
    product_id = create_product(client)

    response = client.post(
        f"/v1/products/{product_id}/offers",
        json={"price_cents": 3900},
    )

    assert response.status_code == 201, response.text
    offer = response.json()
    assert offer["price_cents"] == 3900
    assert offer["currency"] == "BRL"
    assert offer["active"] is True

    event = session.scalar(
        select(OutboxEvent).where(
            OutboxEvent.event_type == "offer.created",
            OutboxEvent.aggregate_id == offer["id"],
        )
    )
    assert event is not None

    result = client.get(f"/v1/products/{product_id}/offers")
    assert result.status_code == 200
    assert len(result.json()) == 1


def test_update_offer(db_client):
    client, _ = db_client
    product_id = create_product(client)

    created = client.post(
        f"/v1/products/{product_id}/offers",
        json={"price_cents": 3900},
    )
    assert created.status_code == 201

    offer_id = created.json()["id"]

    response = client.patch(
        f"/v1/offers/{offer_id}",
        json={
            "price_cents": 4900,
            "active": False,
            "checkout_url": "https://example.com/checkout",
        },
    )

    assert response.status_code == 200, response.text
    assert response.json()["price_cents"] == 4900
    assert response.json()["active"] is False


def test_invalid_checkout_url(db_client):
    client, _ = db_client
    product_id = create_product(client)

    response = client.post(
        f"/v1/products/{product_id}/offers",
        json={
            "price_cents": 3900,
            "checkout_url": "http://example.com/checkout",
        },
    )

    assert response.status_code == 422


def test_unknown_product(db_client):
    client, _ = db_client

    response = client.post(
        f"/v1/products/{uuid4()}/offers",
        json={"price_cents": 3900},
    )

    assert response.status_code == 404


def test_offer_requires_authentication():
    with TestClient(app) as client:
        response = client.get(f"/v1/products/{uuid4()}/offers")

    assert response.status_code == 401


def test_draft_products_not_public():
    with TestClient(app) as client:
        response = client.get("/v1/products")

    assert response.status_code == 401
