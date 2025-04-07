from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserModel(BaseModel):
    description: Optional[str] = Field(description="Info about user")
    username: str = Field(min_length=1)
    first_name: Optional[str]
    last_name: Optional[str]
    hashed_password: str
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode: True
