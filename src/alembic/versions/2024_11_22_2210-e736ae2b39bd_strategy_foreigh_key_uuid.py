"""Strategy foreigh key uuid

Revision ID: e736ae2b39bd
Revises: 452b5bc8a1ee
Create Date: 2024-11-22 22:10:12.278545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e736ae2b39bd'
down_revision: Union[str, None] = '452b5bc8a1ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('strategies', sa.Column('user_uuid', sa.Uuid(), nullable=False))
    op.drop_index('ix_strategies_user_id', table_name='strategies')
    op.drop_constraint('uq_strategies_names_user_ids', 'strategies', type_='unique')
    op.create_unique_constraint('uq_strategies_names_user_ids', 'strategies', ['user_uuid', 'name'])
    op.create_index(op.f('ix_strategies_user_uuid'), 'strategies', ['user_uuid'], unique=False)
    op.drop_constraint('fk_strategies_user_id_users', 'strategies', type_='foreignkey')
    op.create_foreign_key(op.f('fk_strategies_user_uuid_users'), 'strategies', 'users', ['user_uuid'], ['uuid'])
    op.drop_column('strategies', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('strategies', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(op.f('fk_strategies_user_uuid_users'), 'strategies', type_='foreignkey')
    op.create_foreign_key('fk_strategies_user_id_users', 'strategies', 'users', ['user_id'], ['id'])
    op.drop_index(op.f('ix_strategies_user_uuid'), table_name='strategies')
    op.drop_constraint('uq_strategies_names_user_ids', 'strategies', type_='unique')
    op.create_unique_constraint('uq_strategies_names_user_ids', 'strategies', ['user_id', 'name'])
    op.create_index('ix_strategies_user_id', 'strategies', ['user_id'], unique=False)
    op.drop_column('strategies', 'user_uuid')
    # ### end Alembic commands ###
