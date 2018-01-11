"""empty message

Revision ID: ac92de84b8be
Revises: 424fb89f30d0
Create Date: 2017-11-22 19:13:03.637488

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ac92de84b8be'
down_revision = '424fb89f30d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blacklist')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('token', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.Column('blacklist_status', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='blacklist_pkey'),
    sa.UniqueConstraint('token', name='blacklist_token_key')
    )
    # ### end Alembic commands ###