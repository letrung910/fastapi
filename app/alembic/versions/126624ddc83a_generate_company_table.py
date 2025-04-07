"""generate company table

Revision ID: 126624ddc83a
Revises: 
Create Date: 2025-04-01 04:02:49.807302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '126624ddc83a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "company",
        sa.Column("id", sa.UUID, nullable=False, primary_key=True,index=True),
        sa.Column("name", sa.String, nullable=True),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("mode", sa.Integer, nullable=False),
        sa.Column("rating", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True)
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("company")
