from task_manager.exceptions import ValidationError, InvalidStatusError
from task_manager.config import VALID_STATUSES

def validate_title(title: str) -> None:
    if not isinstance(title, str):
        raise ValidationError('Title must be a string')
    elif title.strip() == '':
        raise ValidationError('Title cannot be an empty string')

def validate_description(description: str | None) -> None:
    if description and not isinstance(description, str):
        raise ValidationError('Description must be a string')

def validate_status(status: str) -> None:
    if not isinstance(status, str):
        raise ValidationError('Status must be a string')
    elif status not in VALID_STATUSES:
        raise InvalidStatusError(f"Status must be one of {VALID_STATUSES}")

def validate_task_id(task_id: int) -> None:
    if not isinstance(task_id, int):
        raise ValidationError('Task id must be a integer')
