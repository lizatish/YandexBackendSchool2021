"""Добавление таблицы времени заказов

Revision ID: 82e629e61ca9
Revises: 157c9606cded
Create Date: 2021-03-19 22:45:38.919706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82e629e61ca9'
down_revision = '157c9606cded'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order_assign_time',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time_start_hour', sa.Integer(), nullable=True),
    sa.Column('time_start_min', sa.Integer(), nullable=True),
    sa.Column('time_finish_hour', sa.Integer(), nullable=True),
    sa.Column('time_finish_min', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint(None, 'order', ['order_id'])
    op.drop_column('order', 'time_finish_hour')
    op.drop_column('order', 'time_finish_min')
    op.drop_column('order', 'time_start_hour')
    op.drop_column('order', 'time_start_min')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('time_start_min', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('order', sa.Column('time_start_hour', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('order', sa.Column('time_finish_min', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('order', sa.Column('time_finish_hour', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'order', type_='unique')
    op.drop_table('order_assign_time')
    # ### end Alembic commands ###
