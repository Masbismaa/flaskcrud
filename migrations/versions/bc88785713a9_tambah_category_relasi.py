"""Tambah category relasi

Revision ID: bc88785713a9
Revises: 222f83879117
Create Date: 2026-09-15 14:59:31.639730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc88785713a9'
down_revision = '222f83879117'
branch_labels = None
depends_on = None


def upgrade():

    # 1. Buat tabel category
    op.create_table(
        'category',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 2. Ambil koneksi database
    connection = op.get_bind()

    # 3. Ambil semua kategori unik dari product lama
    result = connection.execute(
        sa.text("SELECT DISTINCT category FROM product")
    )

    categories = [row[0] for row in result]

    # 4. Masukkan kategori lama ke tabel category
    for category_name in categories:
        connection.execute(
            sa.text(
                "INSERT INTO category (name) VALUES (:name)"
            ),
            {"name": category_name}
        )

    # 5. Tambahkan kolom sementara untuk menyimpan category.id
    op.add_column(
        'product',
        sa.Column(
            'category_id',
            sa.Integer(),
            nullable=True
        )
    )

    # 6. Hubungkan product.category lama dengan category.id
    connection.execute(
        sa.text("""
            UPDATE product
            SET category_id = category.id
            FROM category
            WHERE product.category = category.name
        """)
    )

    # 7. Hapus kolom category lama
    op.drop_column('product', 'category')

    # 8. Rename category_id menjadi category
    op.alter_column(
        'product',
        'category_id',
        new_column_name='category'
    )

    # 9. Jadikan category wajib diisi
    op.alter_column(
        'product',
        'category',
        nullable=False
    )

    # 10. Tambahkan foreign key
    op.create_foreign_key(
        'fk_product_category',
        'product',
        'category',
        ['category'],
        ['id']
    )


def downgrade():

    # Ambil koneksi
    connection = op.get_bind()

    # 1. Tambahkan kembali category sebagai text
    op.add_column(
        'product',
        sa.Column(
            'category_name',
            sa.String(length=50),
            nullable=True
        )
    )

    # 2. Kembalikan category.id menjadi category.name
    connection.execute(
        sa.text("""
            UPDATE product
            SET category_name = category.name
            FROM category
            WHERE product.category = category.id
        """)
    )

    # 3. Hapus foreign key
    op.drop_constraint(
        'fk_product_category',
        'product',
        type_='foreignkey'
    )

    # 4. Hapus category integer
    op.drop_column('product', 'category')

    # 5. Rename kembali
    op.alter_column(
        'product',
        'category_name',
        new_column_name='category'
    )

    # 6. Jadikan wajib
    op.alter_column(
        'product',
        'category',
        nullable=False
    )

    # 7. Hapus tabel category
    op.drop_table('category')