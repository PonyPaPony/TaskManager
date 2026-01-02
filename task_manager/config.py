from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent / 'data'
DB_PATH = BASE_DIR / "tasks.db"

# ___ SQL Шаблоны ___
SQL_DEFAULT = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
)
"""

SQL_LOAD_TASKS = """
SELECT id, title, description, status, created_at FROM tasks
"""

SQL_SAVE_TASKS = """
INSERT INTO tasks (id, title, description, status, created_at) VALUES (?, ?, ?, ?, ?)
"""

SQL_DELETE_ALL = """
DELETE FROM tasks
"""

# ___ Valid Status ___
VALID_STATUSES = {'todo', 'in_progress', 'done'}