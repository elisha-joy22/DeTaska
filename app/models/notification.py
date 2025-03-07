from sqlmodel import Field, ForeignKey
from datetime import datetime
from typing import Optional

from app.models.base import BaseModel

class Notification(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(ForeignKey("user.id"))
    message: str
    is_read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    type: str  # Example: "TASK_ASSIGNED", "TASK_COMPLETED", etc.
