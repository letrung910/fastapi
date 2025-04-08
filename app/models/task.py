from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

from sqlalchemy import Enum


class TaskStatus(Enum):
    OPEN = 1
    IN_PROCESS = 2
    COMPLETE = 3

class TaskModel(BaseModel):
    description: Optional[str] = Field(description="Info about Tasks")
    summary: Optional[str]
    status: TaskStatus = Field(default=TaskStatus.OPEN)
    priority: int =  Field(default=1)
    class Config:
        orm_mode: True
