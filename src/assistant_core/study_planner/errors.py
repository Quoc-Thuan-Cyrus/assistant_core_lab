"""Custom exceptions and validation for study planning."""

from .models import Task


class InfeasiblePlan(Exception):
    """Raised when total required task effort exceeds available hours."""

    def __init__(self, needed_h: float, available_h: float) -> None:
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(str(self))

    def __str__(self) -> str:
        return (
            f"Plan is infeasible: need {self.needed_h:.1f} h "
            f"but only {self.available_h:.1f} h available "
            f"(short by {self.needed_h - self.available_h:.1f} h)."
        )


def check_feasible(tasks: list[Task], available_h: float) -> None:
    """Validate whether total effort required by tasks fits within available hours."""
    needed_h = sum(t.effort_h for t in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h=needed_h, available_h=available_h)
