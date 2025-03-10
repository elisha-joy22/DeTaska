from sqlmodel import SQLModel,Field, ForeignKey, Relationship
from typing import List, Optional

from app.models.base import BaseModel
from app.models.status import Status
from app.models.checklist import ChecklistItem


class TaskCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None


class WorkAssignmentDependency(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    work_assignment_id: int = Field(foreign_key="workassignment.id", index=True)
    depends_on_id: int = Field(foreign_key="workassignment.id", index=True)




class WorkAssignment(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(ForeignKey("project.id"))
    work_type_id: int = Field(ForeignKey("work_type.id"))
    space_id: int = Field(ForeignKey("space.id"))
    category_id: Optional[int] = Field(default=None, foreign_key="taskcategory.id")
    order: int = Field(default=1)
    expected_start_date: str
    expected_end_date: str
    actual_start_date: str = None
    actual_end_date: str = None
    expected_cost: float 
    actual_cost: float = 0.0
    status: str = Field(default=Status.PENDING)
    priority: int = Field(default=0)

    category: Optional[TaskCategory] = Relationship(back_populates="work_assignments")
    checklist_items: [ChecklistItem] = Relationship(back_populates="work_assignment")
    dependencies: List["WorkAssignmentDependency"] = Relationship(
        back_populates="dependent_task",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


TaskCategory.work_assignments = Relationship(back_populates="category")