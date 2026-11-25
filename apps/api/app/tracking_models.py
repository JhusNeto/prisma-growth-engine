from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, String, func, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class TrackingEvent(Base):
    __tablename__ = "tracking_events"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    event_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), unique=True)
    event_type: Mapped[str] = mapped_column(String(40), nullable=False)
    product_slug: Mapped[str] = mapped_column(String(80), nullable=False)
    campaign_code: Mapped[str | None] = mapped_column(String(120))
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    consent_given: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
