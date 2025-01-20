"""alter feature table

Revision ID: f3caf22afafa
Revises: 45ac7bb448bb
Create Date: 2025-01-19 16:01:33.144411

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f3caf22afafa"
down_revision: Union[str, None] = "45ac7bb448bb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user_feature", sa.Column("dtype", sa.String(length=100), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user_feature", "dtype")
    # ### end Alembic commands ###
