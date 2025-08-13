"""add foreign key to post table

Revision ID: d69bc7f2a433
Revises: dccfb23b75aa
Create Date: 2025-08-12 12:55:11.019272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd69bc7f2a433'
down_revision: Union[str, Sequence[str], None] = 'dccfb23b75aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_foreign_key(
        'fk_posts_user_id_users',
        'posts',
        'users',
        ['user_id'],
        ['id'],
        ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_posts_user_id_users', 'posts', type_='foreignkey')
    pass
