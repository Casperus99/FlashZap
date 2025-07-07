"""Change next_review_date to Date type

Revision ID: e1e336330745
Revises: 164973c869f4
Create Date: 2025-07-01 22:26:54.785316

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e1e336330745'
down_revision: Union[str, Sequence[str], None] = '164973c869f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('cards', schema=None) as batch_op:
        batch_op.alter_column(
            'next_review_date',
            existing_type=sa.DateTime(),
            type_=sa.Date(),
            existing_nullable=False,
            postgresql_using='next_review_date::date'
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('cards', schema=None) as batch_op:
        batch_op.alter_column(
            'next_review_date',
            existing_type=sa.Date(),
            type_=sa.DateTime(),
            existing_nullable=False,
            postgresql_using='next_review_date::timestamp'
        )
