"""Переименование таблицы

Revision ID: baec42cb43cc
Revises: f6666789e812
Create Date: 2021-03-22 00:17:56.566123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'baec42cb43cc'
down_revision = 'f6666789e812'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('completed_order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('courier_id', sa.Integer(), nullable=True),
    sa.Column('completed_orders', sa.Integer(), nullable=True),
    sa.Column('min_time', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['courier_id'], ['courier.courier_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('completed_orders')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('completed_orders',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('completed_orders', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('min_time', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('courier_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['courier_id'], ['courier.courier_id'], name='completed_orders_courier_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='completed_orders_pkey')
    )
    op.drop_table('completed_order')
    # ### end Alembic commands ###
