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
            "slug": f"page-{uuid4().hex[:12]}",
            "name": "Produto de Teste",
            "audience": "Pequenos empreendedores",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()["id"]


def page_payload():
    return {
        "headline": "Organize seus preços com mais clareza",
        "subheadline": "Uma proposta de apoio para pequenos negócios",
        "description": (
            "Conteúdo demonstrativo utilizado para validar "
            "a API de páginas comerciais do Prisma Growth Engine."
        ),
        "benefits": [
            "Organização das informações comerciais",
            "Apresentação clara dos valores do produto",
        ],
        "faqs": [
            {
                "question": "Como funciona esta solução?",
                "answer": (
                    "Esta é uma página demonstrativa para testes "
                    "de integração da plataforma."
                ),
            }
        ],
        "cta_label": "Conhecer a oferta",
        "seo_title": "Produto demonstrativo | Prisma Dados",
        "seo_description": (
            "Conheça a estrutura de uma página comercial "
            "demonstrativa utilizada nos testes da plataforma."
        ),
    }


def transition(client, product_id, status, checks=None):
    body = {
        "to_status": status,
        "reason": "Validacao automatizada do produto",
    }
    if checks is not None:
        body["checks"] = checks

    return client.post(
        f"/v1/products/{product_id}/transitions",
        json=body,
    )


def test_save_read_and_event(db_client):
    client, session = db_client
    product_id = create_product(client)

    response = client.put(
        f"/v1/products/{product_id}/page",
        json=page_payload(),
    )

    assert response.status_code == 200, response.text
    assert response.json()["approved"] is False

    result = client.get(f"/v1/products/{product_id}/page")
    assert result.status_code == 200
    assert result.json()["headline"] == page_payload()["headline"]

    event = session.scalar(
        select(OutboxEvent).where(
            OutboxEvent.aggregate_id == UUID(product_id),
            OutboxEvent.event_type == "product.page_saved",
        )
    )
    assert event is not None


def test_approval_is_invalidated_on_edit(db_client):
    client, session = db_client
    product_id = create_product(client)
    endpoint = f"/v1/products/{product_id}/page"

    assert client.put(endpoint, json=page_payload()).status_code == 200

    approved = client.post(f"{endpoint}/approve")
    assert approved.status_code == 200, approved.text
    assert approved.json()["approved"] is True
    assert approved.json()["approved_at"] is not None

    changed = page_payload()
    changed["headline"] = "Nova versão da apresentação comercial"

    updated = client.put(endpoint, json=changed)
    assert updated.status_code == 200
    assert updated.json()["approved"] is False
    assert updated.json()["approved_at"] is None

    event = session.scalar(
        select(OutboxEvent).where(
            OutboxEvent.aggregate_id == UUID(product_id),
            OutboxEvent.event_type == "product.page_approved",
        )
    )
    assert event is not None


def test_publication_requires_approved_page(db_client):
    client, _ = db_client
    product_id = create_product(client)

    assert transition(client, product_id, "prepared").status_code == 200

    assert transition(client, product_id, "approved").status_code == 200

    offer = client.post(
        f"/v1/products/{product_id}/offers",
        json={
            "price_cents": 3900,
            "checkout_url": "https://example.com/checkout",
        },
    )
    assert offer.status_code == 201

    checks = {
        "checkout_tested": True,
        "delivery_tested": True,
        "approved_for_publication": True,
    }

    publish = lambda: transition(client, product_id, "live", checks=checks)

    assert publish().status_code == 409

    page_url = f"/v1/products/{product_id}/page"
    assert client.put(page_url, json=page_payload()).status_code == 200

    assert publish().status_code == 409

    assert client.post(f"{page_url}/approve").status_code == 200

    published = publish()
    assert published.status_code == 200, published.text
    assert published.json()["status"] == "live"

    assert client.put(page_url, json=page_payload()).status_code == 409

    assert client.post(f"{page_url}/approve").status_code == 409


def test_archived_product_rejects_content(db_client):
    client, _ = db_client
    product_id = create_product(client)

    assert transition(client, product_id, "archived").status_code == 200

    result = client.put(
        f"/v1/products/{product_id}/page",
        json=page_payload(),
    )
    assert result.status_code == 409


def test_invalid_payload_and_missing_product(db_client):
    client, _ = db_client
    product_id = create_product(client)

    invalid = page_payload()
    invalid["benefits"] = ["curto"]

    response = client.put(
        f"/v1/products/{product_id}/page",
        json=invalid,
    )
    assert response.status_code == 422

    missing = client.put(
        f"/v1/products/{uuid4()}/page",
        json=page_payload(),
    )
    assert missing.status_code == 404


def test_page_requires_authentication():
    with TestClient(app) as client:
        response = client.get(f"/v1/products/{uuid4()}/page")

    assert response.status_code == 401
