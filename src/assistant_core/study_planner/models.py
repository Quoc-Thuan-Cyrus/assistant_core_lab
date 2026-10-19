"""Task dataclass representation for study planning."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """Represents a study task with title, importance, effort (hours), and deadline."""

    title: str
    importance: int
    effort_h: float
    deadline: date

    def days_left(self, today: date | None = None) -> int:
        """Calculate days remaining until task deadline. Never returns below 0."""
        if today is None:
            today = date.today()
        delta = (self.deadline - today).days
        return max(0, delta)
