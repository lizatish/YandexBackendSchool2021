"""Добавление заработка в модель курьера

Revision ID: 4c077b9f2caa
Revises: 8a71156a212a
Create Date: 2021-07-08 21:46:09.667851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c077b9f2caa'
down_revision = '8a71156a212a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courier', sa.Column('earnings', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('courier', 'earnings')
    # ### end Alembic commands ###
