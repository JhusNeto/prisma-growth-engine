from uuid import uuid4

from app.db import get_engine, get_session
from app.main import app
from app.security import require_admin
from app.tracking_models import TrackingEvent
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session


def test_tracking_event_is_idempotent():
    engine = get_engine()
    event_id = uuid4()

    with engine.connect() as connection:
        transaction = connection.begin()
        session = Session(bind=connection, join_transaction_mode="create_savepoint")
        app.dependency_overrides[get_session] = lambda: session
        app.dependency_overrides[require_admin] = lambda: None
        try:
            with TestClient(app) as client:
                payload = {
                    "event_id": str(event_id),
                    "event_type": "checkout_click",
                    "product_slug": "precifica-facil",
                    "occurred_at": "2026-11-16T20:20:00Z",
                    "consent_given": False,
                }
                first = client.post("/v1/events", json=payload)
                duplicate = client.post("/v1/events", json=payload)

            assert first.status_code == 202
            assert first.json()["status"] == "accepted"
            assert duplicate.status_code == 202
            assert duplicate.json()["status"] == "duplicate"
            assert session.scalar(
                select(TrackingEvent).where(TrackingEvent.event_id == event_id)
            ) is not None
        finally:
            app.dependency_overrides.clear()
            session.close()
            transaction.rollback()
