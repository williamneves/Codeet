"""empty message

Revision ID: d85d1e46b18b
Revises: 4db415f28703
Create Date: 2022-03-30 12:43:51.253339

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd85d1e46b18b'
down_revision = '4db415f28703'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('follower', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('follower', sa.Column('id', mysql.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###