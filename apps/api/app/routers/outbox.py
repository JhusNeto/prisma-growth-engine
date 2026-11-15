from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from app.db import get_session
from app.models import OutboxEvent
from app.outbox_schemas import OutboxAckResponse, OutboxEventRead
from app.security import require_admin
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/v1/outbox",
    tags=["outbox"],
    dependencies=[Depends(require_admin)],
)


@router.get(
    "/pending",
    response_model=list[OutboxEventRead],
)
def list_pending_events(
    session: Annotated[Session, Depends(get_session)],
    event_type: Annotated[str | None, Query(min_length=1, max_length=120)] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
) -> list[OutboxEvent]:
    statement = select(OutboxEvent).where(OutboxEvent.published_at.is_(None))

    if event_type is not None:
        statement = statement.where(OutboxEvent.event_type == event_type)

    statement = statement.order_by(
        OutboxEvent.created_at.asc(),
        OutboxEvent.id.asc(),
    ).limit(limit)

    return list(session.scalars(statement).all())


@router.post(
    "/{event_id}/ack",
    response_model=OutboxAckResponse,
)
def acknowledge_event(
    event_id: UUID,
    session: Annotated[Session, Depends(get_session)],
) -> dict:
    event = session.scalar(
        select(OutboxEvent).where(OutboxEvent.id == event_id).with_for_update()
    )

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Outbox event not found",
        )

    if event.published_at is not None:
        return {
            "status": "already_acknowledged",
            "event": event,
        }

    event.published_at = datetime.now(UTC)
    session.commit()
    session.refresh(event)

    return {
        "status": "acknowledged",
        "event": event,
    }
