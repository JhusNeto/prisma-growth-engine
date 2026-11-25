"""Add consent-aware storefront tracking events."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0004_tracking_events"
down_revision = "0003_product_page_content"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tracking_events",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("event_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_type", sa.String(40), nullable=False),
        sa.Column("product_slug", sa.String(80), nullable=False),
        sa.Column("campaign_code", sa.String(120), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consent_given", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.UniqueConstraint("event_id", name="uq_tracking_events_event_id"),
    )


def downgrade() -> None:
    raise RuntimeError("Destructive downgrade of tracking_events is disabled.")
