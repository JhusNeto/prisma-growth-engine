from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import OutboxEvent, Product
from app.schemas import ProductCreate, ProductRead
from app.security import require_admin

router = APIRouter(
    prefix="/v1/products",
    tags=["products"],
    dependencies=[Depends(require_admin)],
)


@router.post(
    "",
    response_model=ProductRead,
    status_code=201,
    dependencies=[Depends(require_admin)],
)
def create_product(
    payload: ProductCreate,
    session: Annotated[Session, Depends(get_session)],
) -> Product:
    product = Product(**payload.model_dump())
    session.add(product)

    try:
        session.flush()

        event = OutboxEvent(
            event_type="product.created",
            aggregate_type="product",
            aggregate_id=product.id,
            payload={
                "product_id": str(product.id),
                "slug": product.slug,
            },
        )
        session.add(event)
        session.commit()

    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Product slug already exists or data conflicts",
        ) from exc

    session.refresh(product)
    return product


@router.get("", response_model=list[ProductRead])
def list_products(
    session: Annotated[Session, Depends(get_session)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Product]:
    statement = (
        select(Product)
        .order_by(Product.created_at.desc(), Product.id.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(session.scalars(statement).all())


@router.get("/{product_id}", response_model=ProductRead)
def get_product(
    product_id: UUID,
    session: Annotated[Session, Depends(get_session)],
) -> Product:
    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product
