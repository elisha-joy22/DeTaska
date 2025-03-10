from sqlmodel import Field, ForeignKey, Relationship

from app.models.base import BaseModel, BaseModelWithTimestamps
from app.models.status import Status

class TaskTracking(BaseModel,BaseModelWithTimestamps, table=True):
    id: int = Field(default=None, primary_key=True)
    work_assignment_id: int = Field(ForeignKey("workassignment.id"))
    checklist_item_id: int = Field(ForeignKey("checklistitem.id"))
    status: Status = Field(default=Status.NOT_STARTED) 
    assigned_person: str = None
    notes: str = None

    checklist_item:"ChecklistItem"=Relationship(back_populates="task_tracking")