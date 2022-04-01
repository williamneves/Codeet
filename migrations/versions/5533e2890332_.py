"""empty message

Revision ID: 5533e2890332
Revises: 20de6fd0c948
Create Date: 2022-03-29 09:39:57.869210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5533e2890332'
down_revision = '20de6fd0c948'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('codeet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('codeet')
    # ### end Alembic commands ###