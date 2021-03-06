"""Добавление связи курьеров и совершенных заказов

Revision ID: f6666789e812
Revises: dc454cbc9a51
Create Date: 2021-03-22 00:13:21.263977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6666789e812'
down_revision = 'dc454cbc9a51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('completed_orders', sa.Column('courier_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'completed_orders', 'courier', ['courier_id'], ['courier_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'completed_orders', type_='foreignkey')
    op.drop_column('completed_orders', 'courier_id')
    # ### end Alembic commands ###
