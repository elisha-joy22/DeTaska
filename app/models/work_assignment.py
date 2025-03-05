from sqlmodel import Field, ForeignKey, Relationship
from typing import List, Optional

from app.models.base import BaseModel
from app.models.status import Status
from app.models.checklist import ChecklistItem


class WorkAssignmentDependency(SQLModel, table=True):
    work_assignment_id: int = Field(ForeignKey("workassignment.id"), primary_key=True)
    depends_on_id: int = Field(ForeignKey("workassignment.id"), primary_key=True)


class WorkAssignment(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(ForeignKey("project.id"))
    work_type_id: int = Field(ForeignKey("work_type.id"))
    space_id: int = Field(ForeignKey("space.id"))
    order: int = Field(default=1)
    expected_start_date: str
    expected_end_date: str
    actual_start_date: str = None
    actual_end_date: str = None
    expected_cost: float 
    actual_cost: float = 0.0
    status: str = Field(default=Status.PENDING)
    priority: int = Field(default=0)

    checklist_items: [ChecklistItem] = Relationship(back_populates="work_assignment")
    dependencies: List["WorkAssignmentDependency"] = Relationship(
        back_populates="dependent_task",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
