"""Command line interface for the Student Task and Study Planner.

Usage:
    python -m src.cli add "Lab report" "Physics" 2026-11-20 --difficulty 4
    python -m src.cli list
    python -m src.cli soon --days 7
    python -m src.cli done 1
"""

import argparse
import json
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import List

from src.planner import Task, due_soon, priority_score, sort_tasks

DATA_FILE = Path("tasks.json")


def load_tasks(path: Path = DATA_FILE) -> List[Task]:
    if not path.exists():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [Task(**{**item, "due": date.fromisoformat(item["due"])}) for item in raw]


def save_tasks(tasks: List[Task], path: Path = DATA_FILE) -> None:
    raw = [{**asdict(t), "due": t.due.isoformat()} for t in tasks]
    path.write_text(json.dumps(raw, indent=2), encoding="utf-8")


def print_tasks(tasks: List[Task], all_tasks: List[Task]) -> None:
    if not tasks:
        print("No tasks to show.")
        return
    for t in tasks:
        number = all_tasks.index(t) + 1
        print(f"[{number}] {t.title} ({t.course}) due {t.due} "
              f"| priority {priority_score(t)}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Student Task and Study Planner")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Add a task")
    add.add_argument("title")
    add.add_argument("course")
    add.add_argument("due", help="Due date as YYYY-MM-DD")
    add.add_argument("--difficulty", type=int, default=3, choices=range(1, 6))

    sub.add_parser("list", help="List unfinished tasks by priority")

    soon = sub.add_parser("soon", help="List tasks due soon")
    soon.add_argument("--days", type=int, default=7)

    done = sub.add_parser("done", help="Mark a task as done")
    done.add_argument("number", type=int, help="Task number from the list")

    return parser


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    tasks = load_tasks()

    if args.command == "add":
        tasks.append(Task(args.title, args.course,
                          date.fromisoformat(args.due), args.difficulty))
        save_tasks(tasks)
        print("Task added.")
    elif args.command == "list":
        print_tasks(sort_tasks(tasks), tasks)
    elif args.command == "soon":
        print_tasks(due_soon(tasks, args.days), tasks)
    elif args.command == "done":
        if not 1 <= args.number <= len(tasks):
            raise SystemExit("No task with that number.")
        tasks[args.number - 1].done = True
        save_tasks(tasks)
        print("Task marked as done.")


if __name__ == "__main__":
    main()
