"""Ensure User model matches Flask-Security-Too requirements

Revision ID: 13c83c53107e
Revises: 7dfcbd72e186
Create Date: 2025-07-07 20:20:15.926526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13c83c53107e'
down_revision = '7dfcbd72e186'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)

    # ### end Alembic commands ###
