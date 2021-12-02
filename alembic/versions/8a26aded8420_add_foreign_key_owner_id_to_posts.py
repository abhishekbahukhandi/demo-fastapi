"""add foreign key:'owner_id' to posts

Revision ID: 8a26aded8420
Revises: 556402c12827
Create Date: 2021-11-30 23:22:42.573511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a26aded8420'
down_revision = '556402c12827'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fkey', 'posts')
    op.drop_column('posts', 'owner_id')
    pass
