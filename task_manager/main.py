import argparse
import sys
from task_manager.services import add_task, list_tasks, remove_task, update_task_status
from task_manager.exceptions import ValidationError, TaskNotFoundError
from task_manager.cli_constants import ID_FLAGS, STATUS_FLAGS, STATUS_CHOICES


def main():
    parser = argparse.ArgumentParser(
        prog="task_manager",
        description="Task Manager CLI"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add")
    add.add_argument('-t', '--title', type=str, required=True, help="Add title")
    add.add_argument("-d", '--description', type=str, required=False, help="Add description")
    add.set_defaults(func=handle_add_task)

    ls = subparsers.add_parser("list")
    ls.add_argument(
        STATUS_FLAGS,
        type=str,
        choices=STATUS_CHOICES,
        help="Show target status"
    )
    ls.set_defaults(func=handle_list)

    up = subparsers.add_parser("update")
    up.add_argument(ID_FLAGS, type=int, required=True, help="Update task id")
    up.add_argument(
        STATUS_FLAGS,
        type=str,
        required=True,
        choices=STATUS_CHOICES,
        help="Update target status"
    )
    up.set_defaults(func=handle_update)

    rm = subparsers.add_parser("remove")
    rm.add_argument(ID_FLAGS, type=int, required=True, help="Remove task id")
    rm.set_defaults(func=handle_remove)

    args = parser.parse_args()

    try:
        args.func(args)
    except ValidationError as e:
        print(e)
        sys.exit(2)
    except TaskNotFoundError as e:
        print(e)
        sys.exit(3)

def handle_add_task(args):
    task = add_task(args.title, args.description)
    print(f"Задача добавлена: id={task.id}")

def handle_list(args):
    tasks = list_tasks(args.status)

    if not tasks:
        print("Задачи не найдены")
        return

    for task in tasks:
        print(f"{task.id} | {task.status} | {task.title}")

def handle_update(args):
    update_task_status(args.id, args.status)
    print(f"Задача {args.id} обновлена")

def handle_remove(args):
    remove_task(args.id)
    print(f"Задача {args.id} удалена")

if __name__ == '__main__':
    main()
