"""mhs_04

Revision ID: 1086441049bc
Revises: 7ed863f2823d
Create Date: 2023-05-03 16:25:07.224392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1086441049bc'
down_revision = '7ed863f2823d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fnc_debt_user', sa.Column('order_id', sa.Integer(), nullable=False))
    op.add_column('fnc_refund', sa.Column('status', sa.String(), nullable=False))
    op.add_column('fnc_refund', sa.Column('refund_by_debt', sa.Integer(), nullable=True))
    op.add_column('fnc_refund', sa.Column('refund_by_rial', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'fnc_refund', ['order_uuid'])
    op.create_unique_constraint(None, 'fnc_refund', ['order_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'fnc_refund', type_='unique')
    op.drop_constraint(None, 'fnc_refund', type_='unique')
    op.drop_column('fnc_refund', 'refund_by_rial')
    op.drop_column('fnc_refund', 'refund_by_debt')
    op.drop_column('fnc_refund', 'status')
    op.drop_column('fnc_debt_user', 'order_id')
    # ### end Alembic commands ###
