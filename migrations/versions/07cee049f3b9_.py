"""empty message

Revision ID: 07cee049f3b9
Revises: 15d9921a2898
Create Date: 2022-03-31 19:27:23.747573

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '07cee049f3b9'
down_revision = '15d9921a2898'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('likes', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('likes', sa.Column('id', mysql.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###