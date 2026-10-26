"""Assistant Core Package — High Maintainability Virtual Assistant Service."""

from .study_planner import InfeasiblePlan, Task, check_feasible, load_tasks, save_json
from .service import AssistantService, build_service
from .models import Message  # (Or .schemas, depending on your Lab 3 file structure)
__all__ = [
    "InfeasiblePlan",
    "Task",
    "check_feasible",
    "load_tasks",
    "save_json",
]
