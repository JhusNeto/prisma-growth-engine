from uuid import UUID, uuid4

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
            "slug": f"lifecycle-{uuid4().hex[:12]}",
            "name": "Produto Lifecycle",
            "audience": "Empreendedores",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()["id"]


def transition(client, product_id, status, **extra):
    return client.post(
        f"/v1/products/{product_id}/transitions",
        json={
            "to_status": status,
            "reason": "Validacao automatizada do ciclo",
            **extra,
        },
    )


def approve_product(client, product_id):
    assert transition(client, product_id, "prepared").status_code == 200
    assert transition(client, product_id, "approved").status_code == 200


def valid_checks():
    return {
        "checkout_tested": True,
        "delivery_tested": True,
        "approved_for_publication": True,
    }


def test_valid_transitions_and_outbox(db_client):
    client, session = db_client
    product_id = create_product(client)

    response = transition(client, product_id, "prepared")

    assert response.status_code == 200
    assert response.json()["status"] == "prepared"

    event = session.scalar(
        select(OutboxEvent).where(
            OutboxEvent.aggregate_id == UUID(product_id),
            OutboxEvent.event_type == "product.status_changed",
        )
    )

    assert event is not None
    assert event.payload["previous_status"] == "draft"
    assert event.payload["new_status"] == "prepared"
    assert event.payload["reason"]


def test_invalid_transition_returns_409(db_client):
    client, _ = db_client
    product_id = create_product(client)

    response = transition(client, product_id, "live")

    assert response.status_code == 409

    result = client.get(f"/v1/products/{product_id}")
    assert result.json()["status"] == "draft"


def test_publication_requires_offer(db_client):
    client, _ = db_client
    product_id = create_product(client)
    approve_product(client, product_id)

    response = transition(
        client,
        product_id,
        "live",
        checks=valid_checks(),
    )

    assert response.status_code == 409


def test_publication_requires_confirmations(db_client):
    client, _ = db_client
    product_id = create_product(client)
    approve_product(client, product_id)

    offer = client.post(
        f"/v1/products/{product_id}/offers",
        json={
            "price_cents": 3900,
            "checkout_url": "https://example.com/checkout",
        },
    )
    assert offer.status_code == 201

    response = transition(client, product_id, "live")
    assert response.status_code == 422


def test_publication_and_commercial_lock(db_client):
    client, _ = db_client
    product_id = create_product(client)

    offer = client.post(
        f"/v1/products/{product_id}/offers",
        json={
            "price_cents": 3900,
            "checkout_url": "https://example.com/checkout",
        },
    )
    assert offer.status_code == 201
    offer_id = offer.json()["id"]

    approve_product(client, product_id)

    published = transition(
        client,
        product_id,
        "live",
        checks=valid_checks(),
    )
    assert published.status_code == 200, published.text
    assert published.json()["status"] == "live"

    update = client.patch(
        f"/v1/offers/{offer_id}",
        json={"price_cents": 4900},
    )
    assert update.status_code == 409

    create = client.post(
        f"/v1/products/{product_id}/offers",
        json={"price_cents": 5000},
    )
    assert create.status_code == 409

    paused = transition(client, product_id, "paused")
    assert paused.status_code == 200

    update = client.patch(
        f"/v1/offers/{offer_id}",
        json={"price_cents": 4900},
    )
    assert update.status_code == 200


def test_archived_is_terminal(db_client):
    client, _ = db_client
    product_id = create_product(client)

    archived = transition(client, product_id, "archived")
    assert archived.status_code == 200
    assert archived.json()["status"] == "archived"

    response = transition(client, product_id, "prepared")
    assert response.status_code == 409


def test_transition_requires_authentication():
    with TestClient(app) as client:
        response = client.post(
            f"/v1/products/{uuid4()}/transitions",
            json={
                "to_status": "prepared",
                "reason": "Operacao nao autorizada",
            },
        )

    assert response.status_code == 401
