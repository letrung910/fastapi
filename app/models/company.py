from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class CompanyModel(BaseModel):
    company_description: Optional[str] = Field(description="Info about company")
    id: UUID
    name: str = Field(min_length=1)
    mode: str
    rating: int
    class Config:
        orm_mode: True
