"""add content column to posts table

Revision ID: 62219d3f6f50
Revises: bd7ec44e0011
Create Date: 2024-03-18 17:51:47.651144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62219d3f6f50'
down_revision: Union[str, None] = 'bd7ec44e0011'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
