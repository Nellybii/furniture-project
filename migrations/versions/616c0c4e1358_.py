"""empty message

Revision ID: 616c0c4e1358
Revises: eb1eaeede207
Create Date: 2024-03-20 14:04:43.950961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '616c0c4e1358'
down_revision = 'eb1eaeede207'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('salt', sa.String(length=32), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('salt')

    # ### end Alembic commands ###
