"""create posts table

Revision ID: a158acc04a35
Revises: 
Create Date: 2021-11-30 21:25:27.723536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a158acc04a35'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True), sa.Column("title", sa.String(), nullable=False))


def downgrade():
    op.drop_table("posts")
