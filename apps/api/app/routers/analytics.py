from typing import Annotated, Literal

from app.analytics_schemas import AnalyticsOverview, OrderRead
from app.commerce_models import Order
from app.db import get_session
from app.models import OutboxEvent, Product
from app.security import require_admin
from fastapi import APIRouter, Depends, Query
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/v1",
    tags=["orders-and-analytics"],
    dependencies=[Depends(require_admin)],
)


@router.get(
    "/orders",
    response_model=list[OrderRead],
)
def list_orders(
    session: Annotated[Session, Depends(get_session)],
    status: Annotated[
        Literal["pending", "approved", "refunded", "chargeback", "cancelled"] | None,
        Query(),
    ] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Order]:
    statement = select(Order)

    if status is not None:
        statement = statement.where(Order.status == status)

    statement = (
        statement.order_by(Order.occurred_at.desc(), Order.id.desc())
        .limit(limit)
        .offset(offset)
    )

    return list(session.scalars(statement).all())


@router.get(
    "/analytics/overview",
    response_model=AnalyticsOverview,
)
def get_analytics_overview(
    session: Annotated[Session, Depends(get_session)],
) -> AnalyticsOverview:
    product_stats = session.execute(
        select(
            func.count(Product.id).label("total"),
            func.coalesce(
                func.sum(case((Product.status == "live", 1), else_=0)),
                0,
            ).label("live"),
        )
    ).one()

    order_stats = session.execute(
        select(
            func.count(Order.id).label("total"),
            func.coalesce(
                func.sum(case((Order.status == "approved", 1), else_=0)),
                0,
            ).label("approved"),
            func.coalesce(
                func.sum(case((Order.status == "pending", 1), else_=0)),
                0,
            ).label("pending"),
            func.coalesce(
                func.sum(case((Order.status == "refunded", 1), else_=0)),
                0,
            ).label("refunded"),
            func.coalesce(
                func.sum(case((Order.status == "chargeback", 1), else_=0)),
                0,
            ).label("chargeback"),
            func.coalesce(
                func.sum(case((Order.status == "cancelled", 1), else_=0)),
                0,
            ).label("cancelled"),
            func.coalesce(
                func.sum(
                    case((Order.status == "approved", Order.amount_cents), else_=0)
                ),
                0,
            ).label("gross_approved_cents"),
            func.coalesce(
                func.sum(
                    case(
                        (
                            Order.status.in_(("refunded", "chargeback")),
                            Order.amount_cents,
                        ),
                        else_=0,
                    )
                ),
                0,
            ).label("reversed_cents"),
        )
    ).one()

    pending_outbox = session.scalar(
        select(func.count(OutboxEvent.id)).where(OutboxEvent.published_at.is_(None))
    ) or 0

    approved_count = int(order_stats.approved)
    gross_approved = int(order_stats.gross_approved_cents)
    reversed_amount = int(order_stats.reversed_cents)
    net_revenue = gross_approved - reversed_amount
    avg_ticket = round(gross_approved / approved_count) if approved_count > 0 else 0

    return AnalyticsOverview(
        total_products=int(product_stats.total),
        live_products=int(product_stats.live),
        total_orders=int(order_stats.total),
        approved_orders=approved_count,
        pending_orders=int(order_stats.pending),
        refunded_orders=int(order_stats.refunded),
        chargeback_orders=int(order_stats.chargeback),
        cancelled_orders=int(order_stats.cancelled),
        gross_approved_cents=gross_approved,
        reversed_cents=reversed_amount,
        net_revenue_cents=net_revenue,
        average_ticket_cents=avg_ticket,
        pending_outbox_events=int(pending_outbox),
    )
