"""create api quota table

Revision ID: 6c812241a1c5
Revises: 0b66bc6e67d3
Create Date: 2021-12-22 20:44:46.295565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c812241a1c5'
down_revision = '0b66bc6e67d3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
      'api_quota',
      sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
      sa.Column('user_id', sa.Integer(), nullable=False),
      sa.Column('api_key', sa.String(length=255), nullable=False),
      sa.Column('quota', sa.Integer(), nullable=False),
      sa.Column('created_at', sa.DateTime(), nullable=True),
      sa.Column('updated_at', sa.DateTime(), nullable=True)
    )


def downgrade():
    op.drop_table('api_quota')
