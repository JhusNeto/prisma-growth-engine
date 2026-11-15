"""Add structured commercial content for product pages."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0003_product_page_content"
down_revision = "0002_product_lifecycle"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "product_pages",
        sa.Column(
            "product_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("products.id"),
            primary_key=True,
        ),
        sa.Column(
            "headline",
            sa.String(160),
            nullable=False,
        ),
        sa.Column(
            "subheadline",
            sa.String(300),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "benefits",
            postgresql.JSONB(),
            nullable=False,
        ),
        sa.Column(
            "faqs",
            postgresql.JSONB(),
            nullable=False,
        ),
        sa.Column(
            "cta_label",
            sa.String(80),
            nullable=False,
        ),
        sa.Column(
            "seo_title",
            sa.String(70),
            nullable=False,
        ),
        sa.Column(
            "seo_description",
            sa.String(160),
            nullable=False,
        ),
        sa.Column(
            "approved",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "approved_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    raise RuntimeError(
        "Destructive downgrade of product_pages is disabled."
    )
