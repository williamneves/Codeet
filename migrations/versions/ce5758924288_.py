"""empty message

Revision ID: ce5758924288
Revises: 054472e6a0d4
Create Date: 2022-03-30 13:39:03.686707

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ce5758924288'
down_revision = '054472e6a0d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_following',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('following_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['following_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'following_id')
    )
    op.drop_table('follower')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follower',
    sa.Column('follower_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('followee_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['followee_id'], ['user.id'], name='follower_ibfk_1'),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], name='follower_ibfk_2'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('user_following')
    # ### end Alembic commands ###