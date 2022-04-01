"""empty message

Revision ID: 3fa951ac61ec
Revises: c7c581369c6d
Create Date: 2022-03-30 14:25:32.934046

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3fa951ac61ec'
down_revision = 'c7c581369c6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follower',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followee_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['followee_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('followers')
    op.add_column('user', sa.Column('Bio', sa.String(length=600), nullable=True))
    op.drop_column('user', 'bio')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('bio', mysql.VARCHAR(length=600), nullable=True))
    op.drop_column('user', 'Bio')
    op.create_table('followers',
    sa.Column('follower_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('followed_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], name='followers_ibfk_1'),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], name='followers_ibfk_2'),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('follower')
    # ### end Alembic commands ###