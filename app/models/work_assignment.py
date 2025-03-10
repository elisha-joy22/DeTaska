from sqlmodel import SQLModel,Field, ForeignKey, Relationship
from typing import List, Optional
from datetime import datetime
from pydantic import field_validator, model_validator

from app.models.base import BaseModel, BaseModelWithTimestamps
from app.models.status import Status
from app.models.checklist import ChecklistItem



class TaskCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None

    work_assignments:List["WorkAssignment"] = Relationship(back_populates="category")

class WorkAssignmentDependency(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    work_assignment_id: int = Field(foreign_key="workassignment.id", index=True, sa_column_kwargs={"ondelete": "CASCADE"} )
    depends_on_id: int = Field(foreign_key="workassignment.id", index=True, sa_column_kwargs={"ondelete": "CASCADE"})




class WorkAssignment(BaseModel, BaseModelWithTimestamps):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(ForeignKey("project.id"),nullable=False)
    work_type_id: int = Field(ForeignKey("work_type.id"),nullable=False)
    space_id: int = Field(ForeignKey("space.id"))
    category_id: Optional[int] = Field(default=None, foreign_key="taskcategory.id")
    order: int = Field(default=1)
    expected_start_date: datetime = Field(default_factory=datetime.utcnow)  
    expected_end_date: datetime = Field(default_factory=datetime.utcnow) 
    actual_start_date: datetime | None = Field(default=None)  
    actual_end_date: datetime | None = Field(default=None)
    expected_cost: Optional[float] = Field(default=0.0, ge=0) 
    actual_cost: Optional[float] = Field(default=0.0, ge=0)
    status: Status = Field(default=Status.NOT_STARTED)
    priority: int = Field(default=0)

    work_type: Optional["WorkType"] = Relationship(back_populates="work_assignments", sa_relationship_kwargs={"cascade": "all, delete"})
    category: Optional[TaskCategory] = Relationship(back_populates="work_assignments")
    checklist_items: [ChecklistItem] = Relationship(back_populates="work_assignment")
    dependencies: List["WorkAssignmentDependency"] = Relationship(
        back_populates="dependent_task",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


    @model_validator(mode="before")
    def validate_dates(cls, values):
        expected_start = values.get("expected_start_date")
        expected_end = values.get("expected_end_date")
        actual_start = values.get("actual_start_date")
        actual_end = values.get("actual_end_date")

        if expected_start and expected_end and expected_start > expected_end:
            raise ValueError("Expected end date must be after expected start date")

        if actual_start and actual_end and actual_start > actual_end:
            raise ValueError("Actual end date must be after actual start date")

        return values
