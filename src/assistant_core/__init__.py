"""Assistant Core Package — High Maintainability Virtual Assistant Service."""

from .models import Message
from .service import AssistantService, build_service
from .study_planner import InfeasiblePlan, Task, check_feasible, load_tasks, save_json

__all__ = [
    "AssistantService",
    "InfeasiblePlan",
    "Message",
    "Task",
    "build_service",
    "check_feasible",
    "load_tasks",
    "save_json",
]
