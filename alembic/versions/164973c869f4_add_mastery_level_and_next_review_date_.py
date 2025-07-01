"""Add mastery_level and next_review_date to cards table

Revision ID: 164973c869f4
Revises: d9421f82299c
Create Date: 2025-06-30 21:17:31.737604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '164973c869f4'
down_revision: Union[str, Sequence[str], None] = 'd9421f82299c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('cards', sa.Column('mastery_level', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('cards', sa.Column('next_review_date', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('cards', 'next_review_date')
    op.drop_column('cards', 'mastery_level')
