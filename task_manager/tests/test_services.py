import pytest

from datetime import datetime
from task_manager import services
from task_manager.config import VALID_STATUSES
from task_manager.exceptions import TaskNotFoundError, InvalidStatusError

def ls_status(status: str | None = None):
    return services.list_tasks(status)

def test_add_task(test_task):
    tasks = services.list_tasks()
    assert len(tasks) == 1
    task = tasks[0]
    assert task.title == 'test_title'
    assert task.description == 'test_description'
    assert task.status == 'todo'
    assert isinstance(task.created_at, datetime)

def test_list_tasks_filter_todo(test_task):
    tasks = ls_status('todo')

    assert len(tasks) == 1
    assert tasks[0].status == 'todo'

def test_list_tasks_filter_done(test_task):
    assert ls_status('done') == []

def test_list_tasks_without_filter(test_task):
    assert len(ls_status()) == 1

def test_update_task(test_task):
    task = ls_status()[0]
    assert task.status == 'todo'

    services.update_task_status(task.id, 'done')

    task = ls_status()[0]
    assert task.status == 'done'

def test_update_task_with_invalid_status(test_task):
    task = ls_status()[0]
    with pytest.raises(InvalidStatusError, match=f"Status must be one of {VALID_STATUSES}"):
        services.update_task_status(task.id, 'invalid')

def test_update_task_with_invalid_id(test_task):
    with pytest.raises(TaskNotFoundError):
        services.update_task_status(999, 'done')

def test_remove_task(test_task):
    task = ls_status()[0]
    services.remove_task(task.id)
    assert ls_status() == []

def test_remove_task_with_invalid_id(test_task):
    with pytest.raises(TaskNotFoundError):
        services.remove_task(999)

    assert len(ls_status()) == 1
    assert ls_status()[0].id != 999