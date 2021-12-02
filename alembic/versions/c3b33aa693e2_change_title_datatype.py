"""change title datatype

Revision ID: c3b33aa693e2
Revises: a223a55d809a
Create Date: 2021-12-02 12:56:55.530635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3b33aa693e2'
down_revision = 'a223a55d809a'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('posts', 'title',
               existing_type=sa.String(),
               nullable=False)
    pass


def downgrade():
    op.alter_column('posts', 'title',
               existing_type=sa.Integer(),
               nullable=False)
    pass
