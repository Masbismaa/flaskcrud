"""Fix sale item quantity column

Revision ID: ca8b87c8032a
Revises: 7a31eaef36c1
Create Date: 2026-09-16 13:41:15.129300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca8b87c8032a'
down_revision = '7a31eaef36c1'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("sale_item", schema=None) as batch_op:
        batch_op.alter_column(
            "quatity",
            new_column_name = "quantity"
        )


def downgrade():
    with op.batch_alter_table("sale_item", schema=None) as batch_op:
        batch_op.alter_column(
            "quantity",
            new_column_name = "quatity"
        )