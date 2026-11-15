from datetime import UTC, datetime
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from app.commerce_models import Order, ProviderEvent
from app.models import Offer, OutboxEvent
from app.webhook_schemas import HotmartWebhookPayload
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

EVENT_TO_ORDER_STATUS: dict[str, str] = {
    "PURCHASE_APPROVED": "approved",
    "PURCHASE_COMPLETE": "approved",
    "PURCHASE_WAITING_PAYMENT": "pending",
    "PURCHASE_BILLET_PRINTED": "pending",
    "PURCHASE_REFUNDED": "refunded",
    "PURCHASE_CHARGEBACK": "chargeback",
    "PURCHASE_PROTEST": "chargeback",
    "PURCHASE_CANCELED": "cancelled",
    "PURCHASE_EXPIRED": "cancelled",
}

STATUS_PRIORITY: dict[str, int] = {
    "pending": 1,
    "cancelled": 2,
    "approved": 3,
    "refunded": 4,
    "chargeback": 4,
}


def to_cents(amount: float) -> int:
    value = Decimal(str(amount)) * Decimal(100)
    return int(value.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def resolve_timestamp(payload: HotmartWebhookPayload) -> datetime:
    raw_ms = (
        payload.data.purchase.approved_date
        or payload.data.purchase.order_date
        or payload.creation_date
    )
    if raw_ms is None:
        return datetime.now(UTC)
    return datetime.fromtimestamp(raw_ms / 1000, tz=UTC)


def resolve_offer_id(session: Session, offer_code: str | None) -> UUID | None:
    if not offer_code:
        return None
    statement = select(Offer.id).where(
        Offer.active.is_(True),
        Offer.checkout_url.ilike(f"%{offer_code}%"),
    )
    return session.scalar(statement)


def sanitize_event_payload(payload: HotmartWebhookPayload) -> dict:
    # Minimização de dados: armazena apenas metadados técnicos da transação, sem PII.
    return {
        "id": payload.id,
        "event": payload.event,
        "version": payload.version,
        "creation_date": payload.creation_date,
        "product": (
            payload.data.product.model_dump(exclude_none=True)
            if payload.data.product
            else None
        ),
        "purchase": {
            "transaction": payload.data.purchase.transaction,
            "status": payload.data.purchase.status,
            "price": payload.data.purchase.price.model_dump(),
            "offer": (
                payload.data.purchase.offer.model_dump(exclude_none=True)
                if payload.data.purchase.offer
                else None
            ),
            "approved_date": payload.data.purchase.approved_date,
            "order_date": payload.data.purchase.order_date,
        },
    }


def process_hotmart_webhook(
    session: Session,
    payload: HotmartWebhookPayload,
) -> dict[str, str | None]:
    order_status = EVENT_TO_ORDER_STATUS.get(payload.event)
    if order_status is None:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported Hotmart event: {payload.event}",
        )

    sanitized = sanitize_event_payload(payload)

    insert_event = (
        pg_insert(ProviderEvent)
        .values(
            provider="hotmart",
            event_id=payload.id,
            event_type=payload.event,
            payload=sanitized,
        )
        .on_conflict_do_nothing(
            index_elements=["provider", "event_id"],
        )
        .returning(ProviderEvent.id)
    )

    inserted_event_id = session.scalar(insert_event)

    if inserted_event_id is None:
        session.commit()
        return {
            "status": "duplicate",
            "event_id": payload.id,
            "order_id": None,
            "order_status": None,
        }

    transaction_id = payload.data.purchase.transaction
    amount_cents = to_cents(payload.data.purchase.price.value)
    occurred_at = resolve_timestamp(payload)
    offer_code = payload.data.purchase.offer.code if payload.data.purchase.offer else None
    offer_id = resolve_offer_id(session, offer_code)

    order = session.scalar(
        select(Order)
        .where(
            Order.provider == "hotmart",
            Order.provider_transaction_id == transaction_id,
        )
        .with_for_update()
    )

    if order is None:
        order = Order(
            provider="hotmart",
            provider_transaction_id=transaction_id,
            offer_id=offer_id,
            amount_cents=amount_cents,
            status=order_status,
            occurred_at=occurred_at,
        )
        session.add(order)
        session.flush()
    else:
        current_rank = STATUS_PRIORITY.get(order.status, 0)
        next_rank = STATUS_PRIORITY.get(order_status, 0)
        if next_rank >= current_rank:
            order.status = order_status
            order.occurred_at = occurred_at
        if order.offer_id is None and offer_id is not None:
            order.offer_id = offer_id

    provider_event = session.get(ProviderEvent, inserted_event_id)
    if provider_event is not None:
        provider_event.processed_at = datetime.now(UTC)

    session.add(
        OutboxEvent(
            event_type=f"order.{order.status}",
            aggregate_type="order",
            aggregate_id=order.id,
            payload={
                "order_id": str(order.id),
                "provider": "hotmart",
                "provider_event_id": payload.id,
                "provider_transaction_id": transaction_id,
                "offer_id": str(order.offer_id) if order.offer_id else None,
                "amount_cents": order.amount_cents,
                "status": order.status,
            },
        )
    )

    session.commit()

    return {
        "status": "processed",
        "event_id": payload.id,
        "order_id": str(order.id),
        "order_status": order.status,
    }
