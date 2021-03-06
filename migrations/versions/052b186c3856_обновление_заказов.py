"""Обновление заказов

Revision ID: 052b186c3856
Revises: 3f4e1ee63f3c
Create Date: 2021-03-18 09:06:04.285041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '052b186c3856'
down_revision = '3f4e1ee63f3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('order_id', sa.Integer(), nullable=False))
    op.drop_column('order', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('order', 'order_id')
    # ### end Alembic commands ###
