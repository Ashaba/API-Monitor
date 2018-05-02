"""empty message

Revision ID: 1ddfa7ff398d
Revises: fac4670c01e6
Create Date: 2018-04-11 15:12:03.208534

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1ddfa7ff398d'
down_revision = '76baf41309fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Collection', sa.Column('interval', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Collection', 'interval')
    # ### end Alembic commands ###
