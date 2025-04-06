from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class CompanyModel(BaseModel):
    description: Optional[str] = Field(description="Info about company")
    # id: UUID
    name: str = Field(min_length=1)
    mode: int = Field(ge=0, le=3, default=0)
    rating: int = Field(ge=0, le=3, default=0)
    class Config:
        orm_mode: True
