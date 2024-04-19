"""create posts table

Revision ID: bd7ec44e0011
Revises: 
Create Date: 2024-03-18 17:24:34.939512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd7ec44e0011'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column("id",sa.Integer(),nullable=False,primary_key=True)
                    ,sa.Column('title',sa.String(),nullable= False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
