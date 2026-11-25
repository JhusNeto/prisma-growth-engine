from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    provider: str
    provider_transaction_id: str
    offer_id: UUID | None
    amount_cents: int
    status: Literal["pending", "approved", "refunded", "chargeback", "cancelled"]
    occurred_at: datetime


class AnalyticsOverview(BaseModel):
    total_products: int
    live_products: int
    total_orders: int
    approved_orders: int
    pending_orders: int
    refunded_orders: int
    chargeback_orders: int
    cancelled_orders: int
    gross_approved_cents: int
    reversed_cents: int
    net_revenue_cents: int
    average_ticket_cents: int
    pending_outbox_events: int
    page_views: int
    checkout_clicks: int
