from typing import Annotated

from app.db import get_session
from app.tracking_models import TrackingEvent
from app.tracking_schemas import TrackingEventAccepted, TrackingEventCreate
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter(prefix="/v1", tags=["tracking"])


@router.post(
    "/events",
    response_model=TrackingEventAccepted,
    status_code=status.HTTP_202_ACCEPTED,
)
def create_tracking_event(
    payload: TrackingEventCreate,
    session: Annotated[Session, Depends(get_session)],
) -> TrackingEventAccepted:
    existing = session.scalar(
        select(TrackingEvent).where(TrackingEvent.event_id == payload.event_id)
    )
    if existing is not None:
        return TrackingEventAccepted(status="duplicate", event_id=payload.event_id)

    session.add(
        TrackingEvent(
            event_id=payload.event_id,
            event_type=payload.event_type,
            product_slug=payload.product_slug,
            campaign_code=payload.campaign_code,
            occurred_at=payload.occurred_at,
            consent_given=payload.consent_given,
        )
    )
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return TrackingEventAccepted(status="duplicate", event_id=payload.event_id)

    return TrackingEventAccepted(status="accepted", event_id=payload.event_id)
