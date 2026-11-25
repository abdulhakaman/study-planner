import pytest

from src.cli import load_tasks, main


@pytest.fixture(autouse=True)
def in_temp_folder(tmp_path, monkeypatch):
    """Run every test in an empty folder so tasks.json is never shared."""
    monkeypatch.chdir(tmp_path)


def add_two_tasks():
    main(["add", "Lab report", "Physics", "2026-12-01"])
    main(["add", "Essay", "History", "2026-12-10", "--difficulty", "2"])


def test_delete_removes_the_chosen_task():
    add_two_tasks()
    main(["delete", "1"])
    tasks = load_tasks()
    assert [t.title for t in tasks] == ["Essay"]


def test_delete_with_bad_number_exits():
    add_two_tasks()
    with pytest.raises(SystemExit):
        main(["delete", "5"])
    assert len(load_tasks()) == 2


def test_edit_changes_only_the_given_fields():
    add_two_tasks()
    main(["edit", "1", "--due", "2026-12-05", "--difficulty", "5"])
    task = load_tasks()[0]
    assert str(task.due) == "2026-12-05"
    assert task.difficulty == 5
    assert task.title == "Lab report"


def test_edit_with_bad_number_exits():
    add_two_tasks()
    with pytest.raises(SystemExit):
        main(["edit", "9", "--title", "X"])