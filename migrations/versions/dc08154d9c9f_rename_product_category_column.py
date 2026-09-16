"""Rename product category column

Revision ID: dc08154d9c9f
Revises: bc88785713a9
Create Date: 2026-09-16 10:05:18.150896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc08154d9c9f'
down_revision = 'bc88785713a9'
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.create_unique_constraint(
            'uq_category_name',
            ['name']
        )

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column(
            'category',
            new_column_name='category_id'
        )


def downgrade():

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column(
            'category_id',
            new_column_name='category'
        )

    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.drop_constraint(
            'uq_category_name',
            type_='unique'
        )