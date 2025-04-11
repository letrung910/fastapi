from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

from sqlalchemy import Enum
import enum

class TaskStatus(enum.Enum):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3

class TaskModel(BaseModel):
    description: Optional[str] = Field(description="Info about Tasks")
    summary: Optional[str]
    status: TaskStatus = Field(default=TaskStatus.TODO)
    priority: int = Field(default=1)
    class Config:
        orm_mode: True


class UpdateTaskModel(BaseModel):
    description: Optional[str] = Field(description="Info about Tasks")
    summary: Optional[str]
    status: TaskStatus = Field(default=TaskStatus.TODO)
    priority: int = Field(default=1)

    class Config:
        orm_mode: True
