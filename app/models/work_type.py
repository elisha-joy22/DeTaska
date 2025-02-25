from sqlmodel import Field

from models.base import BaseModel

class WorkType(BaseModel, table= True):
    id:int = Field(default= None, primary_key=True)
    name: str
    description: str

 