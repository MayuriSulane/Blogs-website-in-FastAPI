"""empty message

Revision ID: 3d8cd49286c8
Revises: 60782f048541
Create Date: 2024-03-19 14:56:22.277487

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d8cd49286c8'
down_revision: Union[str, None] = '60782f048541'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
