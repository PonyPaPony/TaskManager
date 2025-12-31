from datetime import datetime
from task_manager import services


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
    tasks = services.list_tasks()
    task = tasks[0]
    assert task.title == 'test_task'
    assert task.status == 'todo'
    result = services.update_task_status(task.id, 'done')
    assert result is True

    tasks = services.list_tasks()
    task = tasks[0]

    assert task.status == 'done'

def test_update_task_invalid_status(db):
    services.add_task('test_task', 'test_description')
    tasks = services.list_tasks()
    task = tasks[0]
    result = services.update_task_status(task.id, 'invalid')
    assert result is False

def test_update_task_invalid_id(db):
    services.add_task('test_task', 'test_description')
    services.list_tasks()
    result = services.update_task_status(100, 'done')
    assert result is False

def test_remove_task(db):
    services.add_task('test_task', 'test_description')
    tasks = services.list_tasks()
    task = tasks[0]
    result = services.remove_task(task.id)
    assert result is True

def test_remove_task_invalid_id(db):
    services.add_task('test_task', 'test_description')

    result = services.remove_task(999)
    assert result is False

    tasks = services.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == 'test_task'
