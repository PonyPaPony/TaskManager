import logging

from task_manager.models import Task
from task_manager.storage_sqlite import load_tasks, save_tasks
from datetime import datetime

VALID_STATUSES = {"todo", "in_progress", "done"}


def add_task(title: str, description: str | None) -> Task:
    tasks = load_tasks()
    next_id = max((task.id for task in tasks), default=0) + 1
    task = Task(
        id=next_id,
        title=title,
        description=description or "",
        status="todo",
        created_at=datetime.now(),
    )

    tasks.append(task)
    save_tasks(tasks)
    return task

def list_tasks(status: str | None = None) -> list[Task]:
    tasks = load_tasks()

    if status is None:
        return tasks

    if status not in VALID_STATUSES:
        logging.error("Invalid status filter: %s", status)
        return []

    return [task for task in tasks if task.status == status]




def update_task_status(task_id: int, new_status: str) -> bool:
    tasks = load_tasks()

    if new_status not in VALID_STATUSES:
        logging.error("Invalid status: %s", new_status)
        return False

    for task in tasks:
        if task_id != task.id:
            continue
        else:
            task.status = new_status
            save_tasks(tasks)
            return True
    return False

def remove_task(task_id: int) -> bool:
    tasks = load_tasks()

    for task in tasks:
        if task.id != task_id:
            continue
        else:
            tasks.remove(task)
            save_tasks(tasks)
            return True

    return False
