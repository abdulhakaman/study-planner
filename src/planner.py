"""Core logic for the Student Task and Study Planner."""

from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass
class Task:
    title: str
    course: str
    due: date
    difficulty: int = 3  # 1 (easy) to 5 (hard)
    done: bool = False


def priority_score(task: Task, today: Optional[date] = None) -> int:
    """Return a priority score. Higher means more important.

    Rule-based for now: urgency (0-10) plus difficulty (1-5).
    Finished tasks always score 0.
    """
    if task.done:
        return 0
    today = today or date.today()
    days_left = (task.due - today).days
    urgency = 10 if days_left <= 0 else max(0, 10 - days_left)
    return urgency + task.difficulty


def sort_tasks(tasks: List[Task], today: Optional[date] = None) -> List[Task]:
    """Return unfinished tasks sorted from highest to lowest priority."""
    pending = [t for t in tasks if not t.done]
    return sorted(pending, key=lambda t: priority_score(t, today), reverse=True)


def due_soon(tasks: List[Task], days: int = 7, today: Optional[date] = None) -> List[Task]:
    """Return unfinished tasks due within the next `days` days (overdue included)."""
    today = today or date.today()
    return [t for t in tasks if not t.done and (t.due - today).days <= days]
