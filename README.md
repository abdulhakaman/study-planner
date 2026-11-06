# Student Task and Study Planner

A small Python app that helps students track courses, assignments and deadlines. It shows what is due soon and gives every task a priority score so you know what to work on first.

Course project for **Software Engineering Tools and Practices**.

## Features

- Add tasks with a course, due date and difficulty (1 to 5)
- List unfinished tasks sorted by priority
- Show tasks due in the next N days (overdue tasks included)
- Mark tasks as done
- Tasks are saved in a local `tasks.json` file

## How the priority score works

```
priority = urgency + difficulty
urgency  = 10 if due today or overdue, otherwise max(0, 10 - days_left)
```

Finished tasks always score 0.

## Getting started

```bash
git clone <repository-url>
cd study-planner
pip install -r requirements.txt
```

### Usage

```bash
python -m src.cli add "Lab report" "Physics" 2026-11-20 --difficulty 4
python -m src.cli list
python -m src.cli soon --days 7
python -m src.cli done 1
```

### Run the tests

```bash
python -m pytest
```

Tests also run automatically on every push and pull request through GitHub Actions.

## Project structure

```
study-planner/
├── README.md
├── requirements.txt
├── pytest.ini
├── src/
│   ├── planner.py      # core logic: tasks, priority, sorting
│   └── cli.py          # command line interface
├── tests/
│   └── test_planner.py
└── .github/workflows/tests.yml
```

## Team workflow

1. Pick an issue and create a branch: `git checkout -b feature/short-name`
2. Commit small changes with clear messages
3. Push the branch and open a pull request
4. At least one teammate reviews it, then it is merged into `main`
5. Never push directly to `main`

## Team

| Name | Role | GitHub |
|---|---|---|
|Abdulhakim Aman Abdo | Repository owner | abdulhakaman |
| Deng Kuol | Core logic |dengisaac2003-crypto |
|Abdulhakim | Interface |abdulhakaman |
| deng | Testing and CI |dengisaac2003-crypto |

## Planned improvements

- Simple web interface
- Study session reminders
- Replace the rule-based score with a small machine learning model
