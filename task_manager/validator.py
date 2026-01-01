from task_manager.exceptions import ValidationError, InvalidStatusError, TaskNotFoundError

VALID_STATUSES = {"todo", "in_progress", "done"}

def validate_title(title: str) -> None:
    if not isinstance(title, str):
        raise ValidationError("title must be a string")
    elif title.strip() == "":
        raise ValidationError("title cannot be an empty string")

def validate_description(description: str | None) -> None:
    if description and not isinstance(description, str):
        raise ValidationError("description must be a string")

def validate_status(status: str) -> None:
    if not isinstance(status, str):
        raise ValidationError("status must be a string")
    elif status not in VALID_STATUSES:
        raise InvalidStatusError(f"status must be one of {VALID_STATUSES}")

def validate_task_id(task_id: int) -> None:
    if not isinstance(task_id, int):
        raise ValidationError("task id must be a integer")
