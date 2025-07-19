"""adicionando demais colunas do post

Revision ID: be952bedfbb7
Revises: b6a350603d43
Create Date: 2025-07-19 09:58:41.131568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be952bedfbb7'
down_revision: Union[str, Sequence[str], None] = 'b6a350603d43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('is_published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('rating', sa.Integer(), nullable=True, default=0))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))



def downgrade() -> None:
    op.drop_column('posts', 'is_published')
    op.drop_column('posts', 'rating')
    op.drop_column('posts', 'created_at')
