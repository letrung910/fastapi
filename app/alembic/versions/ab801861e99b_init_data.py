"""init data

Revision ID: ab801861e99b
Revises: 791792fa7e6b
Create Date: 2025-04-07 13:16:42.022535

"""
from typing import Sequence, Union
from datetime import datetime, timezone
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

company_id1 = uuid4()
company_id2 = uuid4()
company_id3 = uuid4()

def upgrade() -> None:
    """Upgrade schema."""
    # company
    op.bulk_insert(company_table, [
        {
            "id": company_id1,
            "name": "NashTech1",
            "description": "NashTech1",
            "mode": 1,
            "rating": 1,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        },
        {
            "id": company_id2,
            "name": "NashTech2",
            "description": "NashTech2",
            "mode": 2,
            "rating": 2,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        },
        {
            "id": company_id3,
            "name": "NashTech3",
            "description": "NashTech3",
            "mode": 3,
            "rating": 3,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
    ])

    # user
    op.bulk_insert(user_table , [
            {
                "id": uuid4(),
                "email": "nt1@nt1.com",
                "username": "nt1_admin",
                "hashed_password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
                "first_name": "nt1",
                "last_name": "Admin",
                "is_active": True,
                "is_admin": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "company_id": company_id1
            },
            {
                "id": uuid4(),
                "email": "nt1@nt1.com",
                "username": "nt1",
                "hashed_password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
                "first_name": "nt1",
                "last_name": "nonAdmin",
                "is_active": True,
                "is_admin": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "company_id": company_id1
            },
            {
                "id": uuid4(),
                "email": "nt2@nt2.com",
                "username": "nt2_admin",
                "hashed_password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
                "first_name": "nt2",
                "last_name": "Admin",
                "is_active": True,
                "is_admin": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "company_id": company_id2
            },
            {
                "id": uuid4(),
                "email": "nt2@nt2.com",
                "username": "nt2",
                "hashed_password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
                "first_name": "nt2",
                "last_name": "nonAdmin",
                "is_active": True,
                "is_admin": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "company_id": company_id2
            },
            {
                "id": uuid4(),
                "email": "nt3@nt3.com",
                "username": "nt3_admin",
                "hashed_password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
                "first_name": "nt3",
                "last_name": "Admin",
                "is_active": True,
                "is_admin": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "company_id": company_id3
            }
        ]
    )

def downgrade() -> None:
    """Downgrade schema."""
    pass

