from sqlmodel import SQLModel, Field
from sqlalchemy.orm import event
from datetime import datetime

class BaseModel(SQLModel):
    pass

class BaseModelWithTimestamps(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

# Automatically update `updated_at` before an update occurs
def set_updated_at(mapper, connection, target):
    target.updated_at = datetime.utcnow()

event.listen(BaseModelWithTimestamps, "before_update", set_updated_at)