"""initial migration

Revision ID: 220838e1842f
Revises: 
Create Date: 2019-02-27 18:10:53.568551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '220838e1842f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('symbol', sa.String(length=16), nullable=True),
    sa.Column('exchange', sa.String(length=256), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_companies_name'), 'companies', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_companies_name'), table_name='companies')
    op.drop_table('companies')
    # ### end Alembic commands ###