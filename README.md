# Task Manager CLI

CLI-утилита для управления задачами.
Позволяет добавлять, просматривать, обновлять и удалять задачи.
Данные хранятся локально в SQLite.

## Features

- Add tasks with title and optional description
- List all tasks or filter by status
- Update task status
- Remove tasks
- Persistent storage (SQLite)

## Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/PonyPaPony/TaskManager.git
cd task-manager
pip install -e .
```

---

## Usage

```bash
task-manager <command> [options]
```

---

### Add Task

```bash
task-manager add -t "My task" -d "Optional description"
```

---

### List tasks

```bash
task-manager list
```

---

### Filter by status:

```bash
task-manager list --status todo
```

---

### Update task status

```bash
task-manager update --id 1 --status done
```

---

### Remove task

```bash
task-manager remove --id 1
```

---

## Task statuses

- todo
- in_progress
- done
- 
---

## Error handling

The application uses exit codes:

- `0` — success
- `2` — validation error (invalid input)
- `3` — task not found

```bash
task-manager update --id 999 --status done
# task not found
```

---

## Tests

Run tests with:

```bash
pytest
```
---

## Version

Current version: **v0.1.0**