import sqlite3
from pathlib import Path
from task_manager.models import Task

BASE_DIR = Path.cwd() / "data"  # NOTE: Хочу это вынести в config.py
BASE_DIR.mkdir(parents=True, exist_ok=True)  # +
FILE_PATH = BASE_DIR / "tasks.db"  # +
DB_PATH = FILE_PATH

SQL_LOAD_TASKS = "SELECT id, title, description, status, created_at FROM tasks"
SQL_SAVE_TASKS = "INSERT INTO tasks (id, title, description, status, created_at) VALUES (?, ?, ?, ?, ?)"
SQL_DEFAULT = """CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
SQL_DELETE = "DELETE FROM tasks"
DB_CONNECTION=None


def _get_connection() -> sqlite3.Connection:
    if DB_CONNECTION is not None:
        conn = DB_CONNECTION
    else:
        conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(SQL_DEFAULT)
    return conn

def load_tasks() -> list[Task]:
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            SQL_LOAD_TASKS
        )

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
            cursor.execute(SQL_DELETE)
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