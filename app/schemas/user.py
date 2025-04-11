from database import Base
from .base_entity import BaseEntity
from sqlalchemy import UUID, Column, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship
# Remove circular import
# from schemas import Task

class User(Base, BaseEntity):
    __tablename__ = "user"
    company_id = Column(UUID, ForeignKey("company.id"), nullable=False)
    email = Column(String, nullable=True)
    username = Column(String, nullable=False)
    # id = Column(UUID,nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(String, nullable=False)
    is_admin = Column(String, nullable=False)

    # Fix relationship by using string reference
    tasks = relationship("Task", back_populates="user")
    company = relationship("Company", back_populates="users")
