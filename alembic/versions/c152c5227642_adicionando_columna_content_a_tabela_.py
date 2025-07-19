"""adicionando columna content a tabela posts

Revision ID: c152c5227642
Revises: 20c20b724849
Create Date: 2025-07-19 00:46:49.501477

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c152c5227642'
down_revision: Union[str, Sequence[str], None] = '20c20b724849'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
