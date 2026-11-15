from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OutboxEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    event_type: str
    aggregate_type: str
    aggregate_id: UUID
    payload: dict
    created_at: datetime
    published_at: datetime | None


class OutboxAckResponse(BaseModel):
    status: str
    event: OutboxEventRead
