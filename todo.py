import json
import argparse
import os
from typing import List, Dict

TASKS_FILE = "tasks.json"


def load_tasks() -> List[Dict]:
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks: List[Dict]) -> None:
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def add_task(description: str):
    tasks = load_tasks()
    tasks.append({"description": description, "done": False})
    save_tasks(tasks)
    print(f"✅ Задача добавлена: {description}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("📭 Нет задач")
        return
    for i, task in enumerate(tasks, 1):
        status = "✅" if task["done"] else "🔲"
        print(f"{i}. {status} {task['description']}")


def mark_done(index: int):
    tasks = load_tasks()
    if 0 < index <= len(tasks):
        tasks[index - 1]["done"] = True
        save_tasks(tasks)
        print(f"☑️ Задача {index} отмечена как выполненная.")
    else:
        print("⚠️ Неверный номер задачи.")


def delete_task(index: int):
    tasks = load_tasks()
    if 0 < index <= len(tasks):
        removed = tasks.pop(index - 1)
        save_tasks(tasks)
        print(f"🗑️ Удалена задача: {removed['description']}")
    else:
        print("⚠️ Неверный номер задачи.")


def main():
    parser = argparse.ArgumentParser(description="📝 Менеджер задач CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="Показать список задач")

    add_parser = subparsers.add_parser("add", help="Добавить новую задачу")
    add_parser.add_argument("description", help="Текст задачи")

    done_parser = subparsers.add_parser("done", help="Отметить задачу как выполненную")
    done_parser.add_argument("index", type=int, help="Номер задачи")

    del_parser = subparsers.add_parser("delete", help="Удалить задачу")
    del_parser.add_argument("index", type=int, help="Номер задачи")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        mark_done(args.index)
    elif args.command == "delete":
        delete_task(args.index)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()