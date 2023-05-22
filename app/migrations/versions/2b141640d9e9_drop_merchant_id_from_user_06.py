"""drop_merchant_id_from_user_05

Revision ID: 2b141640d9e9
Revises: adf8a4d56223
Create Date: 2023-05-09 15:31:00.202047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b141640d9e9'
down_revision = 'adf8a4d56223'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usr_user', 'merchant_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usr_user', sa.Column('merchant_id', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###