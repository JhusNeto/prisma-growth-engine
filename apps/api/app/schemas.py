from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class ProductCreate(BaseModel):
    slug: str = Field(
        min_length=3,
        max_length=80,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )
    name: str = Field(min_length=1, max_length=200)
    audience: str = Field(min_length=1, max_length=500)


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    name: str
    audience: str
    status: Literal["draft", "prepared", "approved", "live", "paused", "archived"]
    created_at: datetime
    updated_at: datetime


class SecureCheckoutInput(BaseModel):
    checkout_url: HttpUrl | None = None

    @field_validator("checkout_url")
    @classmethod
    def require_https(cls, value: HttpUrl | None) -> HttpUrl | None:
        if value is not None and value.scheme != "https":
            raise ValueError("Checkout must use HTTPS")
        return value


class OfferCreate(SecureCheckoutInput):
    price_cents: int = Field(gt=0, le=10_000_000)
    currency: Literal["BRL"] = "BRL"


class OfferUpdate(SecureCheckoutInput):
    price_cents: int | None = Field(default=None, gt=0, le=10_000_000)
    active: bool | None = None


class OfferRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    product_id: UUID
    price_cents: int
    currency: str
    checkout_url: str | None
    active: bool


class PublicationChecks(BaseModel):
    checkout_tested: bool
    delivery_tested: bool
    approved_for_publication: bool


class ProductTransition(BaseModel):
    to_status: Literal["draft", "prepared", "approved", "live", "paused", "archived"]
    reason: str = Field(min_length=5, max_length=500)
    checks: PublicationChecks | None = None
