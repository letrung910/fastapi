from database import Base
from .base_entity import BaseEntity
from sqlalchemy import Column


class Company(Base, BaseEntity):
    __tablename__ = "company"
    full_name = Column(str, nullable=False)