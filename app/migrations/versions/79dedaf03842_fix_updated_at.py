"""fix updated_at

Revision ID: 79dedaf03842
Revises: 67553c4fd872
Create Date: 2026-04-04 17:18:12.636129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79dedaf03842'
down_revision = '67553c4fd872'
branch_labels = None
depends_on = None


def upgrade():
    # This migration was generated against a stale DB and duplicated initial tables.
    # Keep it as a no-op so existing installations can advance revision safely.
    pass


def downgrade():
    pass
