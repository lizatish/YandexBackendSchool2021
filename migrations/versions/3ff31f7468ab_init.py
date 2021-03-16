"""Init

Revision ID: 3ff31f7468ab
Revises: 
Create Date: 2021-03-16 10:28:48.579526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ff31f7468ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=30), nullable=True),
    sa.Column('regions', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('working_hours', sa.ARRAY(sa.String(length=30)), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('earnings', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order')
    op.drop_table('courier')
    # ### end Alembic commands ###
