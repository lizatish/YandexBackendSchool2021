"""Укорочение id в БД2

Revision ID: 59f9560d395e
Revises: 035f04ae3366
Create Date: 2021-06-23 12:27:39.079099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59f9560d395e'
down_revision = '035f04ae3366'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courier', sa.Column('id', sa.Integer(), nullable=False))
    op.drop_constraint('courier_courier_id_key', 'courier', type_='unique')
    op.create_unique_constraint(None, 'courier', ['id'])
    op.drop_column('courier', 'courier_id')
    op.add_column('order', sa.Column('id', sa.Integer(), nullable=False))
    op.drop_constraint('order_order_id_key', 'order', type_='unique')
    op.create_unique_constraint(None, 'order', ['id'])
    op.drop_column('order', 'order_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'order', type_='unique')
    op.create_unique_constraint('order_order_id_key', 'order', ['order_id'])
    op.drop_column('order', 'id')
    op.add_column('courier', sa.Column('courier_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'courier', type_='unique')
    op.create_unique_constraint('courier_courier_id_key', 'courier', ['courier_id'])
    op.drop_column('courier', 'id')
    # ### end Alembic commands ###
