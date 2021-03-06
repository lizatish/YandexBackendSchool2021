"""Обнвление названий внутри курьера

Revision ID: 3f4e1ee63f3c
Revises: cf2d95db2e21
Create Date: 2021-03-18 08:33:45.866970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f4e1ee63f3c'
down_revision = 'cf2d95db2e21'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courier', sa.Column('courier_id', sa.Integer(), nullable=False))
    op.add_column('courier', sa.Column('courier_type', sa.String(length=30), nullable=True))
    op.drop_column('courier', 'type')
    op.drop_column('courier', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courier', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.add_column('courier', sa.Column('type', sa.VARCHAR(length=30), autoincrement=False, nullable=True))
    op.drop_column('courier', 'courier_type')
    op.drop_column('courier', 'courier_id')
    # ### end Alembic commands ###
