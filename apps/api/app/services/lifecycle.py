from datetime import UTC, datetime
from urllib.parse import urlsplit
from uuid import UUID

from app.models import Offer, OutboxEvent, Product
from app.page_models import ProductPage
from app.schemas import ProductTransition
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

ALLOWED_TRANSITIONS = {
    "draft": {"prepared", "archived"},
    "prepared": {"draft", "approved", "archived"},
    "approved": {"prepared", "live", "archived"},
    "live": {"paused"},
    "paused": {"live", "archived"},
    "archived": set(),
}


def has_valid_checkout(offer: Offer) -> bool:
    if not offer.active or offer.price_cents <= 0:
        return False

    try:
        parsed = urlsplit(offer.checkout_url or "")
        return (
            parsed.scheme == "https"
            and bool(parsed.hostname)
            and parsed.username is None
            and parsed.password is None
        )
    except ValueError:
        return False


def require_publication_readiness(
    session: Session,
    product_id: UUID,
    payload: ProductTransition,
) -> None:
    checks = payload.checks

    if checks is None or not all(
        (
            checks.checkout_tested,
            checks.delivery_tested,
            checks.approved_for_publication,
        )
    ):
        raise HTTPException(
            status_code=422,
            detail="Publication requires all manual confirmations",
        )

    page = session.get(ProductPage, product_id)

    if page is None or not page.approved:
        raise HTTPException(
            status_code=409,
            detail="Approved commercial content is required",
        )

    offers = session.scalars(select(Offer).where(Offer.product_id == product_id)).all()

    if not any(has_valid_checkout(offer) for offer in offers):
        raise HTTPException(
            status_code=409,
            detail="An active offer with HTTPS checkout is required",
        )


def transition_product(
    session: Session,
    product_id: UUID,
    payload: ProductTransition,
) -> Product:
    product = session.scalar(
        select(Product).where(Product.id == product_id).with_for_update()
    )

    if product is None:
        raise HTTPException(404, "Product not found")

    previous_status = product.status
    next_status = payload.to_status

    if next_status not in ALLOWED_TRANSITIONS[previous_status]:
        raise HTTPException(
            status_code=409,
            detail=(
                f"Transition from {previous_status} to {next_status} is not allowed"
            ),
        )

    if next_status == "live":
        require_publication_readiness(session, product.id, payload)

    product.status = next_status
    product.updated_at = datetime.now(UTC)

    session.add(
        OutboxEvent(
            event_type="product.status_changed",
            aggregate_type="product",
            aggregate_id=product.id,
            payload={
                "product_id": str(product.id),
                "previous_status": previous_status,
                "new_status": next_status,
                "reason": payload.reason,
                "authentication_method": "admin_api_key",
                "publication_checks": (
                    payload.checks.model_dump() if next_status == "live" else None
                ),
            },
        )
    )

    session.commit()
    session.refresh(product)
    return product
