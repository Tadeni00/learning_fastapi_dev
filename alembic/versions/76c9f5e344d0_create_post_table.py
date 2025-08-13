"""create post table

Revision ID: 76c9f5e344d0
Revises: 
Create Date: 2025-08-12 12:18:38.468458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76c9f5e344d0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Upgrade schema."""
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)
    op.create_index(op.f('ix_posts_title'), 'posts', ['title'], unique=False)
    op.create_index(op.f('ix_posts_user_id'), 'posts', ['user_id'], unique=False)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
