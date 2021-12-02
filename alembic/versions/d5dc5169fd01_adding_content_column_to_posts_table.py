"""adding content column to posts table

Revision ID: d5dc5169fd01
Revises: a158acc04a35
Create Date: 2021-11-30 23:01:59.617542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5dc5169fd01'
down_revision = 'a158acc04a35'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", 'content')
    pass
