"""Product class created

Revision ID: 55aa30174a32
Revises: 
Create Date: 2023-09-19 12:49:09.502865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55aa30174a32'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('image', sa.String(length=200), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('size', sa.String(length=200), nullable=False),
    sa.Column('color', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('firstName', sa.String(), nullable=True),
    sa.Column('lastName', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('phone_number', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('products')
    # ### end Alembic commands ###