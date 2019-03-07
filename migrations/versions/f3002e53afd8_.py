"""empty message

Revision ID: f3002e53afd8
Revises: 5aa28adaf212
Create Date: 2019-03-07 12:26:15.316663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3002e53afd8'
down_revision = '5aa28adaf212'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.add_column('portfolios', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'portfolios', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'portfolios', type_='foreignkey')
    op.drop_column('portfolios', 'user_id')
    op.drop_table('users')
    # ### end Alembic commands ###