from sqlmodel import Field, ForeignKey, Relationship
from typing import Optional, List
from datetime import datetime

from app.models.base import BaseModel, BaseModelWithTimestamps
from app.models.status import Status


class ChecklistItem(BaseModel,BaseModelWithTimestamps, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    work_assignment_id: int = Field(ForeignKey("workassignment.id"))
    description: str
    is_mandatory: bool = Field(default=True)
    status: str = Field(default=Status.PENDING) #Pending, In Progress, 
    
    workassignment_id: "WorkAssignment" = Relationship(back_populates="checklist_items")
    task_tracking: List["TaskTracking"] = Relationship(back_populates="checklist_item")


