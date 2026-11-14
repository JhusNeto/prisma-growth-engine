from typing import Annotated
from uuid import UUID

from app.db import get_session
from app.models import Offer, OutboxEvent, Product
from app.schemas import OfferCreate, OfferRead, OfferUpdate
from app.security import require_admin
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/v1",
    tags=["offers"],
    dependencies=[Depends(require_admin)],
)


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
    if session.get(Product, product_id) is None:
        raise HTTPException(404, "Product not found")

    offer = Offer(
        product_id=product_id,
        price_cents=payload.price_cents,
        currency=payload.currency,
        checkout_url=str(payload.checkout_url) if payload.checkout_url else None,
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
        raise HTTPException(404, "Product not found")

    return list(
        session.scalars(
            select(Offer).where(Offer.product_id == product_id).order_by(Offer.id)
        ).all()
    )


@router.patch("/offers/{offer_id}", response_model=OfferRead)
def update_offer(
    offer_id: UUID,
    payload: OfferUpdate,
    session: Annotated[Session, Depends(get_session)],
) -> Offer:
    offer = session.get(Offer, offer_id)

    if offer is None:
        raise HTTPException(404, "Offer not found")

    changes = payload.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(422, "No changes provided")

    for field in ("price_cents", "active"):
        if field in changes and changes[field] is None:
            raise HTTPException(422, f"{field} cannot be null")

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
