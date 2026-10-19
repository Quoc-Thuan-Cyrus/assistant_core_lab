"""Study Planner module — Part of assistant_core project.

Provides Task data structure, persistence (CSV, JSON), and feasibility validation.
"""

from .errors import InfeasiblePlan, check_feasible
from .io_utils import load_tasks, save_json
from .models import Task

__all__ = ["InfeasiblePlan", "Task", "check_feasible", "load_tasks", "save_json"]
