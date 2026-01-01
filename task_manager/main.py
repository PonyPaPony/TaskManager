import argparse
import sys

from task_manager.services import add_task, list_tasks, update_task_status, remove_task
from task_manager.exceptions import ValidationError, TaskNotFoundError


def main():
    parser = argparse.ArgumentParser(
        prog='task_manager',
        description='''Task Manager CLI''',
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    add = subparsers.add_parser("add")
    add.add_argument('-t', '--title', type=str, required=True, help="Add title")
    add.add_argument("-d", '--description', type=str, required=False, help="Add description")
    add.set_defaults(func=handle_add)

    lst = subparsers.add_parser("list")
    lst.add_argument(
        '-s',
        '--status',
        type=str,
        choices=["todo", "in_progress", "done"],
        help="Show target status"
    )
    lst.set_defaults(func=handle_ls)

    update = subparsers.add_parser("update")
    update.add_argument('-i', '--id', type=int, required=True, help="Update target id")
    update.add_argument(
        '-s',
        '--status',
        type=str,
        required=True,
        choices=["todo", "in_progress", "done"],
        help="Update target status"
    )
    update.set_defaults(func=handle_update)

    remove = subparsers.add_parser("remove")
    remove.add_argument('-i', '--id', type=int, required=True, help="Remove target id")
    remove.set_defaults(func=handle_remove)

    args = parser.parse_args()

    try:
        args.func(args)
    except ValidationError as e:
        print(e)
        sys.exit(2)
    except TaskNotFoundError as e:
        print(e)
        sys.exit(3)

def handle_add(args):
    task = add_task(args.title, args.description)
    print(f"Задача добавлена: id={task.id}")

def handle_ls(args):
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