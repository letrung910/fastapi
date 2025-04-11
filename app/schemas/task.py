from database import Base
from .base_entity import BaseEntity
from sqlalchemy import UUID, Column, Numeric, String, ForeignKey
from sqlalchemy.types import Enum
from sqlalchemy.orm import relationship
from models.task import TaskStatus
# import enum


class Task(Base, BaseEntity):
    __tablename__ = "task"
    id = Column(UUID, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    # company_id = Column(UUID, nullable=False)
    summary = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), nullable=False)
    priority = Column(Numeric, nullable=False)

    # Fix relationship by using string reference
    user = relationship("User", back_populates="tasks")
