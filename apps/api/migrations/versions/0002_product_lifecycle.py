"""Add archived product status."""

import sqlalchemy as sa
from alembic import op

revision = "0002_product_lifecycle"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None

OLD_STATUSES = (
    "'draft','prepared','approved','live','paused'"
)

NEW_STATUSES = (
    "'draft','prepared','approved','live','paused','archived'"
)


def upgrade() -> None:
    op.drop_constraint(
        "products_status_check",
        "products",
        type_="check",
    )
    op.create_check_constraint(
        "products_status_check",
        "products",
        f"status IN ({NEW_STATUSES})",
    )


def downgrade() -> None:
    connection = op.get_bind()

    archived = connection.execute(
        sa.text(
            "SELECT count(*) FROM products "
            "WHERE status = 'archived'"
        )
    ).scalar_one()

    if archived:
        raise RuntimeError(
            "Cannot downgrade while archived products exist."
        )

    op.drop_constraint(
        "products_status_check",
        "products",
        type_="check",
    )
    op.create_check_constraint(
        "products_status_check",
        "products",
        f"status IN ({OLD_STATUSES})",
    )
