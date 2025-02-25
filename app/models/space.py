from sqlmodel import Field, ForeignKey

from models.base import BaseModel
from models.status import Status

class Space(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    parent_space_id: int = Field(ForeignKey("space.id"), nullable=True)
    type: str
    status: str = Field(default=Status.PENDING)