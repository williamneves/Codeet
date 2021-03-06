"""empty message

Revision ID: d6049f449a07
Revises: ce5758924288
Create Date: 2022-03-30 13:40:38.385393

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd6049f449a07'
down_revision = 'ce5758924288'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follower',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followee_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['followee_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    op.drop_table('user_following')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_following',
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('following_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['following_id'], ['user.id'], name='user_following_ibfk_1'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='user_following_ibfk_2'),
    sa.PrimaryKeyConstraint('user_id', 'following_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('follower')
    # ### end Alembic commands ###
