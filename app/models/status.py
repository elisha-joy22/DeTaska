from enum import Enum

class Status(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    NOT_STARTED = "Not Started"

    @classmethod
    def list(cls):
        return [cls.PENDING, cls.IN_PROGRESS, cls.COMPLETED]

    @classmethod
    def is_valid(cls, status: str):
        return status in cls.list()
