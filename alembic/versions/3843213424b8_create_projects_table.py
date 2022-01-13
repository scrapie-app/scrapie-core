"""create projects table

Revision ID: 3843213424b8
Revises: 6c812241a1c5
Create Date: 2022-01-11 01:29:17.535097

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null

# revision identifiers, used by Alembic.
revision = '3843213424b8'
down_revision = '6c812241a1c5'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('api_key_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

def downgrade():
    op.drop_table('projects')
