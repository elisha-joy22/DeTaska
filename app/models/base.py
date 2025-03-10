from sqlmodel import SQLModel, Field
from sqlalchemy.orm import event
from datetime import datetime

class BaseModel(SQLModel):
    pass

class BaseModelWithTimestamps(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


@event.listens_for(BaseModelWithTimestamps, "before_update", propagate=True)
def update_timestamp(mapper, connection, target):
    target.updated_at = datetime.utcnow()