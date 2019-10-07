"""empty message

Revision ID: 0b4f76ca6d36
Revises: 
Create Date: 2019-10-07 18:51:36.093039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b4f76ca6d36'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('picture', sa.Column('label', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('picture', 'label')
    # ### end Alembic commands ###
