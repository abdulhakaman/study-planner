from datetime import date

from src.planner import Task, due_soon, priority_score, sort_tasks

TODAY = date(2026, 11, 5)


def make(title, days_from_today, difficulty=3, done=False):
    due = date.fromordinal(TODAY.toordinal() + days_from_today)
    return Task(title, "Course", due, difficulty, done)


def test_done_task_scores_zero():
    assert priority_score(make("a", 1, done=True), TODAY) == 0


def test_overdue_task_gets_max_urgency():
    assert priority_score(make("a", -3, difficulty=2), TODAY) == 12


def test_far_deadline_has_no_urgency():
    assert priority_score(make("a", 30, difficulty=4), TODAY) == 4


def test_closer_deadline_scores_higher():
    near = priority_score(make("near", 1), TODAY)
    far = priority_score(make("far", 8), TODAY)
    assert near > far


def test_sort_tasks_orders_by_priority_and_skips_done():
    tasks = [make("far", 10), make("done", 0, done=True), make("near", 1)]
    result = sort_tasks(tasks, TODAY)
    assert [t.title for t in result] == ["near", "far"]


def test_due_soon_includes_overdue_and_excludes_later():
    tasks = [make("overdue", -2), make("soon", 3), make("later", 20)]
    result = due_soon(tasks, days=7, today=TODAY)
    assert [t.title for t in result] == ["overdue", "soon"]
