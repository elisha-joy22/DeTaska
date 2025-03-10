from sqlmodel import Field
from app.models.base import BaseModel, BaseModelWithTimestamps

from app.models.base import BaseModel

class WorkType(BaseModel,BaseModelWithTimestamps, table= True):
    id:int = Field(default= None, primary_key=True)
    name: str
    description: str

