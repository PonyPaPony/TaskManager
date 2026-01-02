import sqlite3
from task_manager.models import Task
from task_manager.config import DB_PATH, BASE_DIR, SQL_DEFAULT, SQL_LOAD_TASKS, SQL_DELETE_ALL, SQL_SAVE_TASKS


DB_CONNECTION = None

def _get_connection() -> sqlite3.Connection:
    if DB_CONNECTION is not None:
        conn = DB_CONNECTION
    else:
        BASE_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row
    conn.execute(SQL_DEFAULT)
    return conn

def load_tasks() -> list[Task]:
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(SQL_LOAD_TASKS)
        rows = cursor.fetchall()

        return [Task.from_row(row) for row in rows]
    finally:
        if DB_CONNECTION is None:
            conn.close()

def save_tasks(tasks: list[Task]) -> None:
    conn = _get_connection()

    try:
        cursor = conn.cursor()
        with conn:
            cursor.execute(SQL_DELETE_ALL)
            cursor.executemany(SQL_SAVE_TASKS,
                               [
                                   (
                                       task.id,
                                       task.title,
                                       task.description,
                                       task.status,
                                       task.serialize_created_at(),
                                   )
                                   for task in tasks
                               ],
                               )
    finally:
        if DB_CONNECTION is None:
            conn.close()