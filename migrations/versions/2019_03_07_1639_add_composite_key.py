"""empty message

Revision ID: 2019_03_07_add_composite_key
Revises: 6cd356f29e22
Create Date: 2019-03-07 16:15:23.339928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2019_03_07_add_composite_key'
down_revision = '6cd356f29e22'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE companies ADD PRIMARY KEY (name, portfolio_id);')


def downgrade():
    op.execute('ALTER TABLE companies DROP CONSTRAINT companies_pkey;')
