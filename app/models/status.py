class Status:
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

    @classmethod
    def list(cls):
        return [cls.PENDING, cls.IN_PROGRESS, cls.COMPLETED]

    @classmethod
    def is_valid(cls, status: str):
        return status in cls.list()
