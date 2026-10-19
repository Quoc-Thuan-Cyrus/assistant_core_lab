"""Tests for study_planner module integration."""

from datetime import date

import pytest

from assistant_core.study_planner import InfeasiblePlan, Task, check_feasible, load_tasks, save_json


def test_task_days_left():
    task = Task("Exam", importance=5, effort_h=4.0, deadline=date(2026, 10, 25))
    today = date(2026, 10, 20)
    assert task.days_left(today) == 5

    # Past deadline returns 0
    past_today = date(2026, 10, 30)
    assert task.days_left(past_today) == 0


def test_check_feasible():
    tasks = [
        Task("Task 1", 3, 2.5, date(2026, 10, 25)),
        Task("Task 2", 4, 3.5, date(2026, 10, 26)),
    ]
    # Total effort: 6.0 h
    check_feasible(tasks, available_h=7.0)  # Should pass

    with pytest.raises(InfeasiblePlan) as exc_info:
        check_feasible(tasks, available_h=5.0)
    assert "short by 1.0 h" in str(exc_info.value)


def test_load_and_save_tasks(tmp_path):
    csv_file = tmp_path / "tasks.csv"
    csv_file.write_text(
        "title,importance,effort_h,deadline\nMath Test,5,4.0,2026-10-25\nEssay,4,2.5,2026-10-27\n",
        encoding="utf-8",
    )

    tasks = load_tasks(csv_file)
    assert len(tasks) == 2
    assert tasks[0].title == "Math Test"
    assert tasks[0].importance == 5

    json_file = tmp_path / "tasks.json"
    save_json(tasks, json_file)
    assert json_file.exists()
    content = json_file.read_text(encoding="utf-8")
    assert "Math Test" in content
