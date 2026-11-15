from datetime import datetime
from uuid import UUID

from app.models import Base
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column


class ProductPage(Base):
    __tablename__ = "product_pages"

    product_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("products.id"),
        primary_key=True,
    )
    headline: Mapped[str] = mapped_column(String(160), nullable=False)
    subheadline: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    benefits: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    faqs: Mapped[list[dict]] = mapped_column(JSONB, nullable=False)
    cta_label: Mapped[str] = mapped_column(String(80), nullable=False)
    seo_title: Mapped[str] = mapped_column(String(70), nullable=False)
    seo_description: Mapped[str] = mapped_column(String(160), nullable=False)

    approved: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )
    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
