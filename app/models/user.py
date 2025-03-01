from sqlmodel import SQLModel, Field
from enum import Enum

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MANAGER = "manager"

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False, index=True)
    name: str = Field(default="")
    profile_pic: str = Field(default="")
    role: Role = Field(default=Role.USER)
