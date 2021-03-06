"""добавление основных таблиц 

Revision ID: cf2d95db2e21
Revises: 3ff31f7468ab
Create Date: 2021-03-17 19:12:49.257157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf2d95db2e21'
down_revision = '3ff31f7468ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('delivery_hours', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('order', sa.Column('region', sa.Integer(), nullable=True))
    op.add_column('order', sa.Column('weight', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'weight')
    op.drop_column('order', 'region')
    op.drop_column('order', 'delivery_hours')
    # ### end Alembic commands ###
