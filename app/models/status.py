from enum import Enum

class Status():
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

    @classmethod
    def list(cls):
        return [cls.PENDING, cls.IN_PROGRESS, cls.COMPLETED]

    @classmethod
    def is_valid(cls, status: str):
        return status in cls.list()
