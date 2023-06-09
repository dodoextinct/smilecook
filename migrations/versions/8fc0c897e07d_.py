"""empty message

Revision ID: 8fc0c897e07d
Revises: 1cf0dd244be3
Create Date: 2023-06-07 07:03:55.684619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fc0c897e07d'
down_revision = '1cf0dd244be3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ingredients', sa.String(length=1000), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.drop_column('ingredients')

    # ### end Alembic commands ###
