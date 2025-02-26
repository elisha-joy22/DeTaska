from sqlmodel import Field, ForeignKey

from app.models.base import BaseModel

class WorkAssignment(BaseModel):
    id: int = Field(default=None, primary_key=True)
    project_id: int = Field(ForeignKey("project.id"))
    work_type_id: int = Field(ForeignKey("work_type.id"))
    space_id: int = Field(ForeignKey("space.id"))
    order: int = Field(default=1)
    expected_start_date: str
    expected_end_date: str
    actual_start_date: str = None
    actual_end_date: str = None
    expected_cost: float = 0.0
