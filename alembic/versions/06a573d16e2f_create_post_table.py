"""create post table

Revision ID: 06a573d16e2f
Revises: 
Create Date: 2026-02-18 14:56:50.457512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06a573d16e2f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),sa.Column('title',sa.String(),nullable=False))
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
