from task_manager.models import Task
from task_manager.storage_sqlite import load_tasks, save_tasks
from task_manager.validator import validate_task_id, validate_status, validate_title, validate_description
from task_manager.exceptions import TaskNotFoundError
from datetime import datetime

def add_task(title: str, description: str | None) -> Task:
    validate_title(title)
    validate_description(description)

    tasks = load_tasks()
    next_id = max((task.id for task in tasks), default=0) + 1
    task = Task(
        id=next_id,
        title=title,
        description=description or None,
        status="todo",
        created_at=datetime.now(),
    )

    tasks.append(task)
    save_tasks(tasks)
    return task

def list_tasks(status: str | None = None) -> list[Task]:
    if status is not None:
        validate_status(status)

    tasks = load_tasks()

    if status is None:
        return tasks

    return [task for task in tasks if task.status == status]




def update_task_status(task_id: int, new_status: str):
    tasks = load_tasks()

    validate_task_id(task_id)
    validate_status(new_status)

    found = False

    for task in tasks:
        if task_id != task.id:
            continue
        else:
            found = True
            task.status = new_status
            save_tasks(tasks)
            break

    if not found:
        raise TaskNotFoundError("task not found")

def remove_task(task_id: int):
    validate_task_id(task_id)
    tasks = load_tasks()

    found = False

    for task in tasks:
        if task.id == task_id:
            found = True
            tasks.remove(task)
            save_tasks(tasks)
            break

    if not found:
        raise TaskNotFoundError("task not found")