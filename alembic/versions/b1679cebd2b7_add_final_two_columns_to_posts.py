"""add final two columns to posts

Revision ID: b1679cebd2b7
Revises: 8a26aded8420
Create Date: 2021-11-30 23:39:59.593772

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision = 'b1679cebd2b7'
down_revision = '8a26aded8420'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default='True', nullable=False),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'),))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
