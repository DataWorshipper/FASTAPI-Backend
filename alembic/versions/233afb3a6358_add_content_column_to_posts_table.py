"""add content column to posts table

Revision ID: 233afb3a6358
Revises: 06a573d16e2f
Create Date: 2026-02-18 15:33:59.173284

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '233afb3a6358'
down_revision: Union[str, Sequence[str], None] = '06a573d16e2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
