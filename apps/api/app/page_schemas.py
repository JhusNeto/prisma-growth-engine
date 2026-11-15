from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


class FAQEntry(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    question: str = Field(min_length=8, max_length=200)
    answer: str = Field(min_length=12, max_length=1500)


BenefitText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=8,
        max_length=180,
    ),
]


class ProductPageWrite(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    headline: str = Field(min_length=10, max_length=160)
    subheadline: str = Field(min_length=15, max_length=300)
    description: str = Field(min_length=40)
    benefits: list[BenefitText] = Field(min_length=2, max_length=8)
    faqs: list[FAQEntry] = Field(min_length=1, max_length=8)
    cta_label: str = Field(min_length=3, max_length=80)
    seo_title: str = Field(min_length=10, max_length=70)
    seo_description: str = Field(min_length=50, max_length=160)


class ProductPageRead(ProductPageWrite):
    model_config = ConfigDict(from_attributes=True)

    product_id: UUID
    approved: bool
    approved_at: datetime | None
    created_at: datetime
    updated_at: datetime
