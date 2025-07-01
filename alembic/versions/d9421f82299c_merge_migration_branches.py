"""Merge migration branches

Revision ID: d9421f82299c
Revises: 62941882f6f4, be04b522466d
Create Date: 2025-06-30 21:17:08.057147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9421f82299c'
down_revision: Union[str, Sequence[str], None] = ('62941882f6f4', 'be04b522466d')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
