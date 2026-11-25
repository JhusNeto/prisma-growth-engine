from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import OutboxEvent, Product
from app.page_models import ProductPage
from app.page_schemas import ProductPageRead, ProductPageWrite
from app.security import require_admin

router = APIRouter(
    prefix="/v1/products",
    tags=["product-pages"],
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
        raise HTTPException(404, "Product not found")

    if product.status in ("live", "archived"):
        raise HTTPException(
            409,
            "Pause published products before editing. "
            "Archived products cannot be edited.",
        )

    return product


@router.put(
    "/{product_id}/page",
    response_model=ProductPageRead,
)
def save_product_page(
    product_id: UUID,
    payload: ProductPageWrite,
    session: Annotated[Session, Depends(get_session)],
) -> ProductPage:
    require_editable_product(session, product_id)

    page = session.get(ProductPage, product_id)
    values = payload.model_dump()

    if page is None:
        page = ProductPage(
            product_id=product_id,
            **values,
        )
        session.add(page)
    else:
        for field, value in values.items():
            setattr(page, field, value)

    # Qualquer gravação invalida uma aprovação anterior.
    page.approved = False
    page.approved_at = None
    page.updated_at = datetime.now(UTC)

    session.add(
        OutboxEvent(
            event_type="product.page_saved",
            aggregate_type="product",
            aggregate_id=product_id,
            payload={
                "product_id": str(product_id),
                "approved": False,
            },
        )
    )

    session.commit()
    session.refresh(page)
    return page


@router.get(
    "/{product_id}/page",
    response_model=ProductPageRead,
)
def get_product_page(
    product_id: UUID,
    session: Annotated[Session, Depends(get_session)],
) -> ProductPage:
    page = session.get(ProductPage, product_id)

    if page is None:
        raise HTTPException(404, "Product page not found")

    return page


@router.post(
    "/{product_id}/page/approve",
    response_model=ProductPageRead,
)
def approve_product_page(
    product_id: UUID,
    session: Annotated[Session, Depends(get_session)],
) -> ProductPage:
    require_editable_product(session, product_id)

    page = session.get(ProductPage, product_id)

    if page is None:
        raise HTTPException(404, "Product page not found")

    if page.approved:
        raise HTTPException(409, "Product page already approved")

    now = datetime.now(UTC)

    page.approved = True
    page.approved_at = now
    page.updated_at = now

    session.add(
        OutboxEvent(
            event_type="product.page_approved",
            aggregate_type="product",
            aggregate_id=product_id,
            payload={
                "product_id": str(product_id),
                "approved_at": now.isoformat(),
            },
        )
    )

    session.commit()
    session.refresh(page)
    return page
