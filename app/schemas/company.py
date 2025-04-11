from database import Base
from .base_entity import BaseEntity
from sqlalchemy import UUID, Column, Numeric, String
from sqlalchemy.orm import relationship

class Company(Base, BaseEntity):
    __tablename__ = "company"
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    mode = Column(String, nullable=False)
    rating = Column(Numeric, nullable=False)

    users = relationship("User", back_populates="company")