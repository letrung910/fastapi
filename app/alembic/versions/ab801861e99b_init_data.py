"""init data

Revision ID: ab801861e99b
Revises: 791792fa7e6b
Create Date: 2025-04-07 13:16:42.022535

"""
from typing import Sequence, Union
from datetime import datetime
from alembic import op
import sqlalchemy as sa
from uuid import uuid4
from services.hash_service import get_password_hash
from settings import ADMIN_DEFAULT_PASSWORD
from sqlalchemy import Table, MetaData

# revision identifiers, used by Alembic.
revision: str = 'ab801861e99b'
down_revision: Union[str, None] = '791792fa7e6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# get metadata from current connection
meta = MetaData()
# pass in tuple with tables we want to reflect, otherwise whole database will get reflected
meta.reflect(only=('company', 'user',), bind=op.get_bind())

company_table = Table('company', meta)
user_table = Table('user', meta)

def upgrade() -> None:
    """Upgrade schema."""
    company_id = uuid4()
    print(f'{company_id}')
    # company
    op.bulk_insert(company_table, [
        {
            "id": company_id,
            "name": "NashTech",
            "description": "NashTech Company",
            "mode": 1,
            "rating": 5,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
    ])

    # user
    op.bulk_insert(user_table , [
            {
                "id": uuid4(),
                "email": "fastapi@fastapi.com",
                "username": "fastapi_admin",
                "hashed_password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
                "first_name": "FastApi",
                "last_name": "Admin",
                "is_active": True,
                "is_admin": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "company_id": company_id
            }
        ]
    )

def downgrade() -> None:
    """Downgrade schema."""
    pass

