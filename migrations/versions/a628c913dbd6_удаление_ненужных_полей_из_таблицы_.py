"""Удаление ненужных полей из таблицы курьера

Revision ID: a628c913dbd6
Revises: 517d4de5acd8
Create Date: 2021-03-22 00:39:45.087886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a628c913dbd6'
down_revision = '517d4de5acd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('courier', 'earnings')
    op.drop_column('courier', 'rating')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courier', sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('courier', sa.Column('earnings', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
