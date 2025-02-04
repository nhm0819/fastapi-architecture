"""add column in feature table - size

Revision ID: 9b9790ebebb9
Revises: f3caf22afafa
Create Date: 2025-01-21 16:28:24.096633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b9790ebebb9'
down_revision: Union[str, None] = 'f3caf22afafa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_feature', sa.Column('size', sa.Integer(), nullable=False))
    op.alter_column('user_feature', 'bvector',
               existing_type=sa.VARBINARY(length=4096),
               type_=sa.VARBINARY(length=32768),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_feature', 'bvector',
               existing_type=sa.VARBINARY(length=32768),
               type_=sa.VARBINARY(length=4096),
               existing_nullable=False)
    op.drop_column('user_feature', 'size')
    # ### end Alembic commands ###
