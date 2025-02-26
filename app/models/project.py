from sqlmodel import Field

from app.models.base import BaseModel

class Project(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    address: str = None
    start_date: str
    end_date: str = None
    estimated_budget: float
    actual_budget:float = None
