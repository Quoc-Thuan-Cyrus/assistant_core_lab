"""I/O utilities for loading and saving tasks."""

import csv
import json
from datetime import date
from pathlib import Path

from .models import Task


def load_tasks(path: str | Path) -> list[Task]:
    """Load tasks from a CSV file with header: title,importance,effort_h,deadline.

    Raises:
        ValueError: If a row contains invalid data, reporting the line number.
    """
    tasks = []
    path = Path(path)

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line_num, row in enumerate(reader, start=2):  # header is line 1
            try:
                title = row["title"].strip()
                importance = int(row["importance"].strip())
                effort_h = float(row["effort_h"].strip())
                deadline = date.fromisoformat(row["deadline"].strip())
                tasks.append(
                    Task(title=title, importance=importance, effort_h=effort_h, deadline=deadline)
                )
            except (KeyError, ValueError) as e:
                raise ValueError(f"Invalid data on line {line_num}: {e}") from e

    return tasks


def save_json(tasks: list[Task], path: str | Path) -> None:
    """Save a list of Task objects to a formatted JSON file."""
    path = Path(path)
    data = [
        {
            "title": t.title,
            "importance": t.importance,
            "effort_h": t.effort_h,
            "deadline": t.deadline.isoformat(),
        }
        for t in tasks
    ]
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
