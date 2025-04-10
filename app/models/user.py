from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserModel(BaseModel):
    username: str = Field(min_length=1)
    email: str
    id: UUID
    company_id: Optional[UUID]
    first_name: Optional[str]
    last_name: Optional[str]
    hashed_password: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: Optional[datetime]
    class Config:
        orm_mode: True


class CreateUserModel(BaseModel):
    username: str = Field(min_length=1)
    email: str
    company_id: UUID
    first_name: Optional[str]
    last_name: Optional[str]
    password: str
    repeat_password: str
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode: True


class UpdateUserModel(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    is_admin: bool
    updated_at: Optional[datetime]
    class Config:
        orm_mode: True


class UpdatePasswordUserModel(BaseModel):
    password: str
    repeat_password: str
    updated_at: Optional[datetime]
    class Config:
        orm_mode: True
