from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

from app.models.base import BaseModel, BaseModelWithTimestamps
from app.models.user import User
from app.models.project import Project
from app.models.space import Space
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task(BaseModel,BaseModelWithTimestamps, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    
    project_id: int = Field(foreign_key="project.id")
    work_type_id: int = Field(foreign_key="worktype.id")
    space_id: Optional[int] = Field(foreign_key="space.id", default=None)
    
    assigned_to: Optional[int] = Field(foreign_key="user.id", default=None)
    
    expected_start: datetime = Field(nullable=True)
    actual_start: datetime = Field(nullable=True, default=None)
    expected_end: datetime = Field(nullable=True)
    actual_end: datetime = Field(nullable=True, default=None)
    
    expected_cost: float = Field(default=0.0)
    actual_cost: float = Field(default=0.0)
    
    project: Optional["Project"] = Relationship(back_populates="tasks")
    work_type: Optional["WorkType"] = Relationship(back_populates="tasks")
    space: Optional["Space"] = Relationship(back_populates="tasks")
    assigned_user: Optional["User"] = Relationship(back_populates="tasks")
