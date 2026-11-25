from datetime import UTC, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class TrackingEventCreate(BaseModel):
    event_id: UUID
    event_type: Literal["page_view", "checkout_click"]
    product_slug: str = Field(
        min_length=3,
        max_length=80,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )
    campaign_code: str | None = Field(default=None, max_length=120)
    occurred_at: datetime
    consent_given: bool = False

    @classmethod
    def normalize_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value

    def model_post_init(self, __context: object, /) -> None:
        self.occurred_at = self.normalize_timestamp(self.occurred_at)


class TrackingEventAccepted(BaseModel):
    status: Literal["accepted", "duplicate"]
    event_id: UUID
