"""delete posts table

Revision ID: 5437dd5d1e12
Revises: c3b33aa693e2
Create Date: 2021-12-02 13:05:44.449112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5437dd5d1e12'
down_revision = 'c3b33aa693e2'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("posts")
    pass


def downgrade():
    op.create_table("posts", sa.Column("id", sa.Integer(), primary_key=True, nullable=False))
    pass
