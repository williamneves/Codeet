"""empty message

Revision ID: 324e0470ce1c
Revises: f3165f66fb2f
Create Date: 2022-04-03 00:54:40.902239

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '324e0470ce1c'
down_revision = 'f3165f66fb2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('codeet', sa.Column('re_codeet', sa.Boolean(), nullable=True))
    op.drop_constraint('codeet_ibfk_1', 'codeet', type_='foreignkey')
    op.create_foreign_key(None, 'codeet', 'user', ['user_id'], ['id'])
    op.add_column('user', sa.Column('name', sa.String(length=255), nullable=True))
    op.add_column('user', sa.Column('github', sa.String(length=255), nullable=True))
    op.add_column('user', sa.Column('site', sa.String(length=255), nullable=True))
    op.drop_column('user', 'first_name')
    op.drop_column('user', 'last_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_name', mysql.VARCHAR(length=255), nullable=True))
    op.add_column('user', sa.Column('first_name', mysql.VARCHAR(length=255), nullable=True))
    op.drop_column('user', 'site')
    op.drop_column('user', 'github')
    op.drop_column('user', 'name')
    op.drop_constraint(None, 'codeet', type_='foreignkey')
    op.create_foreign_key('codeet_ibfk_1', 'codeet', 'user', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('codeet', 're_codeet')
    # ### end Alembic commands ###
