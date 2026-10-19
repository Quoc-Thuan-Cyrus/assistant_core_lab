# Lưu ý: Lớp Rule này thường được định nghĩa trong models.py hoặc knowledge.py (phần Handbook).
# Ở đây ta định nghĩa tạm một dataclass để code không bị lỗi cú pháp khi gọi thuộc tính.
from dataclasses import dataclass
from typing import Protocol

from assistant_core.errors import ProviderError


@dataclass
class Rule:
    id: str
    title: str
    text: str


class Responder(Protocol):
    def explain(self, question: str, rule: Rule) -> str: ...


class TemplateResponder:
    def explain(self, question: str, rule: Rule) -> str:
        return f"{rule.title}: {rule.text}"


class StubLLMResponder:
    def __init__(self, fail: bool = False):
        self.fail = fail

    def explain(self, question: str, rule: Rule) -> str:
        if self.fail:
            raise ProviderError("stub provider unavailable")
        return f"Based on '{rule.title}': {rule.text}"
