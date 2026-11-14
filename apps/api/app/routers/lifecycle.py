from typing import Annotated
from uuid import UUID

from app.db import get_session
from app.schemas import ProductRead, ProductTransition
from app.security import require_admin
from app.services.lifecycle import transition_product
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/v1/products",
    tags=["product-lifecycle"],
    dependencies=[Depends(require_admin)],
)


@router.post(
    "/{product_id}/transitions",
    response_model=ProductRead,
)
def change_product_status(
    product_id: UUID,
    payload: ProductTransition,
    session: Annotated[Session, Depends(get_session)],
):
    return transition_product(session, product_id, payload)
