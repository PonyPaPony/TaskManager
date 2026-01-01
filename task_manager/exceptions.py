class TaskManagerError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class ValidationError(TaskManagerError):
    pass

class InvalidStatusError(TaskManagerError):
    pass

class TaskNotFoundError(TaskManagerError):
    pass