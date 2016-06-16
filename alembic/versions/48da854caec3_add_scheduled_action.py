"""add scheduled action

Revision ID: 48da854caec3
Revises: 5303e5ca6b1b
Create Date: 2016-06-16 11:38:23.539127

"""

# revision identifiers, used by Alembic.
revision = '48da854caec3'
down_revision = '5303e5ca6b1b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scheduled_actions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('action_date', sa.DateTime(), nullable=False),
    sa.Column('in_progress', sa.Boolean(), nullable=True),
    sa.Column('interval_in_second', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scheduled_actions')
    ### end Alembic commands ###