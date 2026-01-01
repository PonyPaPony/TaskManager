import pytest

from datetime import datetime
from task_manager import services
from task_manager.validator import VALID_STATUSES
from task_manager.exceptions import TaskNotFoundError, InvalidStatusError

def test_add_task(db):
    test_title = 'test_task'
    test_description = 'test_description'
    services.add_task(test_title, test_description)  # Создаем задачу

    tasks = services.list_tasks()  # Загружаем ее
    assert len(tasks) == 1
    task = tasks[0]
    assert task.title == test_title
    assert task.description == test_description
    assert task.status == 'todo'
    assert isinstance(task.created_at, datetime)

def test_list_tasks_filter_todo(db):
    services.add_task('test_task', 'test_description')

    tasks = services.list_tasks('todo')  # есть совпадение

    assert len(tasks) == 1
    assert tasks[0].status == 'todo'

def test_list_tasks_filter_done(db):
    services.add_task('test_task', 'test_description')
    tasks = services.list_tasks('done')  # нет совпадений

    assert tasks == []

def test_list_tasks_without_filter(db):
    services.add_task('test_task', 'test_description')
    tasks = services.list_tasks()  # без фильтра

    assert len(tasks) == 1

def test_update_task(db):
    services.add_task('test_task', 'test_description')

    task = services.list_tasks()[0]
    assert task.status == 'todo'

    services.update_task_status(task.id, 'done')

    task = services.list_tasks()[0]
    assert task.status == 'done'

def test_update_task_invalid_status(db):
    services.add_task('test_task', 'test_description')
    tasks = services.list_tasks()
    task = tasks[0]
    with pytest.raises(InvalidStatusError, match=f"status must be one of {VALID_STATUSES}"):
        services.update_task_status(task.id, 'invalid')

def test_update_task_invalid_id(db):
    services.add_task('test_task', 'test_description')
    with pytest.raises(TaskNotFoundError):
        services.update_task_status(100, 'done')

def test_remove_task(db):
    services.add_task('test_task', 'test_description')

    task = services.list_tasks()[0]
    services.remove_task(task.id)

    assert services.list_tasks() == []

def test_remove_task_invalid_id(db):
    services.add_task('test_task', 'test_description')

    with pytest.raises(TaskNotFoundError):
        services.remove_task(999)

    tasks = services.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].id != 999
