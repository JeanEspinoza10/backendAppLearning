"""empty message

Revision ID: e216989a0a5a
Revises: bdb5f7786d65
Create Date: 2024-09-24 08:58:21.299759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e216989a0a5a'
down_revision = 'bdb5f7786d65'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=140), nullable=True))
        batch_op.add_column(sa.Column('password', sa.String(length=120), nullable=False))
        batch_op.create_unique_constraint(None, ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('password')
        batch_op.drop_column('email')

    # ### end Alembic commands ###