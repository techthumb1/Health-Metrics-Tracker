"""Increase password_hash length

Revision ID: 34556268cde3
Revises: 
Create Date: 2024-11-10 15:55:16.585922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34556268cde3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=150),
               type_=sa.String(length=512),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=512),
               type_=sa.VARCHAR(length=150),
               existing_nullable=False)

    # ### end Alembic commands ###
