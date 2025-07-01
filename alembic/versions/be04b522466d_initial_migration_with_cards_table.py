"""Initial migration with cards table

Revision ID: be04b522466d
Revises: 
Create Date: 2025-06-30 21:20:25.305948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be04b522466d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('cards',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('front', sa.String(length=200), nullable=False),
        sa.Column('back', sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('cards')
