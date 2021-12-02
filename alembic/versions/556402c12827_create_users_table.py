"""create users table

Revision ID: 556402c12827
Revises: d5dc5169fd01
Create Date: 2021-11-30 23:11:12.007760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '556402c12827'
down_revision = 'd5dc5169fd01'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('email', sa.String(), nullable=False, unique=True), sa.Column('password', sa.String(), nullable=False), sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade():
    op.drop_table('users')
    pass
