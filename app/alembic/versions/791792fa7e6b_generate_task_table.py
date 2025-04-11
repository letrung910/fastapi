"""generate task table

Revision ID: 791792fa7e6b
Revises: bbac0d9ae811
Create Date: 2025-04-01 07:14:33.211788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from schemas.task import TaskStatus
from sqlalchemy import Enum

# revision identifiers, used by Alembic.
revision: str = '791792fa7e6b'
down_revision: Union[str, None] = 'bbac0d9ae811'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "task",
        sa.Column("id", sa.UUID, nullable=False, primary_key=True, index=True),
        sa.Column("user_id", sa.UUID, nullable=True),
        sa.Column("summary", sa.String, nullable= True),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("status", sa.Enum(TaskStatus), nullable=False),
        sa.Column("priority", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True)
    )

    op.create_foreign_key(
        'fk_task_user',
        'task', 'user',
        ['user_id'], ['id'],
    )
def downgrade() -> None:
    """Downgrade schema."""
    pass
