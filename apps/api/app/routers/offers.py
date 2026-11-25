from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Offer, OutboxEvent, Product
from app.schemas import OfferCreate, OfferRead, OfferUpdate
from app.security import require_admin

router = APIRouter(
    prefix="/v1",
    tags=["offers"],
    dependencies=[Depends(require_admin)],
)


def require_editable_product(
    session: Session,
    product_id: UUID,
) -> Product:
    product = session.scalar(
        select(Product).where(Product.id == product_id).with_for_update()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    if product.status == "live":
        raise HTTPException(
            status_code=409,
            detail="Pause product before editing offers",
        )

    return product


@router.post(
    "/products/{product_id}/offers",
    response_model=OfferRead,
    status_code=201,
)
def create_offer(
    product_id: UUID,
    payload: OfferCreate,
    session: Annotated[Session, Depends(get_session)],
) -> Offer:
    require_editable_product(session, product_id)

    offer = Offer(
        product_id=product_id,
        price_cents=payload.price_cents,
        currency=payload.currency,
        checkout_url=(str(payload.checkout_url) if payload.checkout_url else None),
        active=True,
    )

    session.add(offer)
    session.flush()

    session.add(
        OutboxEvent(
            event_type="offer.created",
            aggregate_type="offer",
            aggregate_id=offer.id,
            payload={
                "offer_id": str(offer.id),
                "product_id": str(product_id),
            },
        )
    )

    session.commit()
    session.refresh(offer)

    return offer


@router.get(
    "/products/{product_id}/offers",
    response_model=list[OfferRead],
)
def list_offers(
    product_id: UUID,
    session: Annotated[Session, Depends(get_session)],
) -> list[Offer]:
    if session.get(Product, product_id) is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    statement = select(Offer).where(Offer.product_id == product_id).order_by(Offer.id)

    return list(session.scalars(statement).all())


@router.patch(
    "/offers/{offer_id}",
    response_model=OfferRead,
)
def update_offer(
    offer_id: UUID,
    payload: OfferUpdate,
    session: Annotated[Session, Depends(get_session)],
) -> Offer:
    offer = session.get(Offer, offer_id)

    if offer is None:
        raise HTTPException(
            status_code=404,
            detail="Offer not found",
        )

    require_editable_product(session, offer.product_id)

    changes = payload.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=422,
            detail="No changes provided",
        )

    for field in ("price_cents", "active"):
        if field in changes and changes[field] is None:
            raise HTTPException(
                status_code=422,
                detail=f"{field} cannot be null",
            )

    if "checkout_url" in changes and changes["checkout_url"] is not None:
        changes["checkout_url"] = str(changes["checkout_url"])

    for field, value in changes.items():
        setattr(offer, field, value)

    session.add(
        OutboxEvent(
            event_type="offer.updated",
            aggregate_type="offer",
            aggregate_id=offer.id,
            payload={
                "offer_id": str(offer.id),
                "changed_fields": sorted(changes),
            },
        )
    )

    session.commit()
    session.refresh(offer)

    return offer
