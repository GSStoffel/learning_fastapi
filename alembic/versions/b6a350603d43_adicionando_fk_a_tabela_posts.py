"""adicionando fk a tabela posts

Revision ID: b6a350603d43
Revises: a849fbe4ae82
Create Date: 2025-07-19 09:46:50.073116

"""
from tkinter.constants import CASCADE
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6a350603d43'
down_revision: Union[str, Sequence[str], None] = 'a849fbe4ae82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")



def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
