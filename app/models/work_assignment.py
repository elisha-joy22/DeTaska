from sqlmodel import SQLModel,Field, ForeignKey, Relationship
from typing import List, Optional
from datetime import datetime

from app.models.base import BaseModel
from app.models.status import Status
from app.models.checklist import ChecklistItem


class TaskCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None


class WorkAssignmentDependency(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    work_assignment_id: int = Field(foreign_key="workassignment.id", index=True, sa_column_kwargs={"ondelete": "CASCADE"} )
    depends_on_id: int = Field(foreign_key="workassignment.id", index=True, sa_column_kwargs={"ondelete": "CASCADE"})




class WorkAssignment(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(ForeignKey("project.id"))
    work_type_id: int = Field(ForeignKey("work_type.id"))
    space_id: int = Field(ForeignKey("space.id"))
    category_id: Optional[int] = Field(default=None, foreign_key="taskcategory.id")
    order: int = Field(default=1)
    expected_start_date: Optional[datetime] = Field(default=None)  # Can be null
    expected_end_date: Optional[datetime] = Field(default=None)  
    actual_start_date: Optional[datetime] = Field(default=None)
    actual_end_date: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow) 
    expected_cost: float 
    actual_cost: float = 0.0
    status: Status = Field(default=Status.PENDING)
    priority: int = Field(default=0)

    category: Optional[TaskCategory] = Relationship(back_populates="work_assignments")
    checklist_items: [ChecklistItem] = Relationship(back_populates="work_assignment")
    dependencies: List["WorkAssignmentDependency"] = Relationship(
        back_populates="dependent_task",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


TaskCategory.work_assignments = Relationship(back_populates="category")