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
    engine = get_engine()

    with engine.connect() as connection:
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


def test_product_creation_and_outbox(db_client):
    client, session = db_client
    slug = f"produto-{uuid4().hex[:12]}"

    response = client.post(
        "/v1/products",
        json={
            "slug": slug,
            "name": "Produto de Teste",
            "audience": "Pequenos comerciantes",
        },
    )

    assert response.status_code == 201, response.text

    data = response.json()
    assert data["slug"] == slug
    assert data["status"] == "draft"

    product_id = UUID(data["id"])

    event = session.scalar(
        select(OutboxEvent).where(OutboxEvent.aggregate_id == product_id)
    )

    assert event is not None
    assert event.event_type == "product.created"
    assert event.payload["product_id"] == str(product_id)

    detail = client.get(f"/v1/products/{product_id}")
    assert detail.status_code == 200

    listing = client.get("/v1/products")
    assert listing.status_code == 200
    assert any(item["id"] == str(product_id) for item in listing.json())


def test_duplicate_slug_returns_409(db_client):
    client, _ = db_client

    payload = {
        "slug": f"produto-{uuid4().hex[:12]}",
        "name": "Produto Teste",
        "audience": "Empreendedores",
    }

    first = client.post("/v1/products", json=payload)
    second = client.post("/v1/products", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409


def test_invalid_slug_returns_422(db_client):
    client, _ = db_client

    response = client.post(
        "/v1/products",
        json={
            "slug": "Slug Inválido",
            "name": "Produto",
            "audience": "Empreendedores",
        },
    )

    assert response.status_code == 422


def test_unknown_product_returns_404(db_client):
    client, _ = db_client

    response = client.get(f"/v1/products/{uuid4()}")
    assert response.status_code == 404


def test_write_requires_admin_key():
    with TestClient(app) as client:
        response = client.post(
            "/v1/products",
            json={
                "slug": "teste-sem-chave",
                "name": "Produto",
                "audience": "Empreendedores",
            },
        )

    assert response.status_code == 401
