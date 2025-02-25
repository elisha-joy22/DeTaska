from sqlmodel import Field, ForeignKey

from models.base import BaseModel
from models.status import Status

class TaskTracking(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    work_assignment_id: int = Field(ForeignKey("workassignment.id"))
    checklist_item_id: int = Field(ForeignKey("checklistitem.id"))
    status: str = Field(default=Status.PENDING) 
    assigned_person: str = None
    notes: str = None
