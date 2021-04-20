"""Initial

Revision ID: 88392ccd0bba
Revises: 
Create Date: 2021-04-20 17:55:18.072938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88392ccd0bba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('commands',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=4), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_commands_id'), 'commands', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_commands_id'), table_name='commands')
    op.drop_table('commands')
    # ### end Alembic commands ###
