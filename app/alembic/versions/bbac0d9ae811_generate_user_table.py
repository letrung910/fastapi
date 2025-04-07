"""generate user table

Revision ID: bbac0d9ae811
Revises: 126624ddc83a
Create Date: 2025-04-01 07:14:28.931315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bbac0d9ae811'
down_revision: Union[str, None] = '126624ddc83a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "user",
        sa.Column("id", sa.UUID, nullable=False, primary_key=True, index=True),
        sa.Column("company_id", sa.UUID, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("username", sa.String, nullable=False),
        sa.Column("first_name", sa.String, nullable=True),
        sa.Column("last_name", sa.String, nullable=True),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False),
        sa.Column("is_admin", sa.Boolean, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True)
        )

    op.create_foreign_key(
        'fk_user_company',
        'user', 'company',
        ['company_id'], ['id'],
    )
def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user")
