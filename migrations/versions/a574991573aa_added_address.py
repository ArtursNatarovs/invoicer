"""added address

Revision ID: a574991573aa
Revises: 8f7ca3e82928
Create Date: 2020-09-16 20:29:32.307502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a574991573aa'
down_revision = '8f7ca3e82928'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('salon', sa.Column('city', sa.String(), nullable=True))
    op.add_column('salon', sa.Column('line1', sa.String(), nullable=True))
    op.add_column('salon', sa.Column('line2', sa.String(), nullable=True))
    op.add_column('salon', sa.Column('postCode', sa.String(), nullable=True))
    op.add_column('users', sa.Column('city', sa.String(), nullable=True))
    op.add_column('users', sa.Column('line1', sa.String(), nullable=True))
    op.add_column('users', sa.Column('line2', sa.String(), nullable=True))
    op.add_column('users', sa.Column('postCode', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'postCode')
    op.drop_column('users', 'line2')
    op.drop_column('users', 'line1')
    op.drop_column('users', 'city')
    op.drop_column('salon', 'postCode')
    op.drop_column('salon', 'line2')
    op.drop_column('salon', 'line1')
    op.drop_column('salon', 'city')
    # ### end Alembic commands ###
