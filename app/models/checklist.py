from sqlmodel import Field, ForeignKey

from models.base import BaseModel
from models.status import Status


class ChecklistItem(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    work_type_id: int = Field(ForeignKey("worktype.id"))
    description: str
    is_mandatory: bool = Field(default=True)
    status: str = Field(default=Status.PENDING) #Pending, In Progress, Completed
