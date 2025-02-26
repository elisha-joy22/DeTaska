from sqlmodel import Field, ForeignKey
from .base import BaseModel

class Expense(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    work_assignment_id: int = Field(ForeignKey("workassignment.id"))
    expense_type: str  # Material, Labor, Miscellaneous
    estimated_cost: float
    actual_cost: float = 0.0
    date: str