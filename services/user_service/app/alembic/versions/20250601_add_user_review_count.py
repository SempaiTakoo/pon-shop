"""add user review count table

Revision ID: 20250601_add_user_review_count
Revises: 877a705ce7f6
Create Date: 2025-06-01
"""
from alembic import op
import sqlalchemy as sa

revision = '20250601_add_user_review_count'
down_revision = '877a705ce7f6'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'UserReviewCount',
        sa.Column('user_id', sa.Integer(), primary_key=True),
        sa.Column('review_count', sa.Integer(), nullable=False, server_default='0'),
    )

def downgrade() -> None:
    op.drop_table('UserReviewCount')
