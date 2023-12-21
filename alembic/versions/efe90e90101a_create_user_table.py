"""Create user tables

Revision ID: efe90e90101a
Revises: 
Create Date: 2023-12-18 00:56:33.814311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'efe90e90101a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = ("main", )
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('password', sa.String(128), nullable=False),
        sa.Column('salt', sa.String(50), nullable=False),
        sa.Column('createdAt', sa.DateTime, nullable=False),
        sa.Column('lastEdited', sa.DateTime, nullable=False),
    )

    op.create_table(
        'groups',
        sa.Column('_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('createdAt', sa.DateTime, nullable=False),
        sa.Column('lastEdited', sa.DateTime, nullable=False),
    )

    op.create_table(
        'pivot_users_groups',
        sa.Column('_id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users._id')),
        sa.Column('group_id', sa.Integer, sa.ForeignKey('groups._id')),
        sa.Column('lastEdited', sa.DateTime, nullable=False),
    )

def downgrade():
    op.drop_table('pivot_users_groups')
    op.drop_table('groups')
    op.drop_table('users')