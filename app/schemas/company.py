from database import Base
from .base_entity import BaseEntity
from sqlalchemy import UUID, Column, Numeric, String


class Company(Base, BaseEntity):
    __tablename__ = "company"
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    mode = Column(String, nullable=False)
    rating = Column(Numeric, nullable=False)

