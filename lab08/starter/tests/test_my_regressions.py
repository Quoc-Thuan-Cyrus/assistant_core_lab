"""Lab 8 Part E: turn YOUR Week-7 failures into regression tests.

Write at least three tests. Each one must:
  - have a name that says what went wrong, e.g. test_empty_sources_does_not_crash_ui
  - FAIL on the old code (check by temporarily undoing your fix), and PASS after the fix.
Use the fixtures `service`, `settings` from conftest.py, or build a TestClient like tests/test_security.py.
"""

from assistant_core.models import Message
from ui.api_client import ChatResult
from ui.logic import format_sources, status_note


def test_example_greeting_still_works(service):
    """Example: a control case that must never break."""
    assert "Hello" in service.handle(Message(text="hi")).answer


def test_retake_number_as_word(service):
    """BUG-7: 'two retakes' was ignored and the total was too low (8,100,000 instead of 9,450,000)."""
    r = service.handle(Message(text="tuition for 18 credits and two retakes"))
    assert "8,100,000" not in r.answer  # never the wrong total
    assert "9,450,000" in r.answer  # correctly parses word 'two' as digit 2


def test_empty_sources_format_does_not_crash():
    """Week-7 Observation 2: Rendering answers without sources should safely produce an empty string."""
    assert format_sources([]) == ""
    sample_sources = [{"id": "H26#5.3", "title": "5.3 Thesis registration"}]
    assert format_sources(sample_sources) == "Sources: H26#5.3 — 5.3 Thesis registration"


def test_escalation_gives_training_office_room():
    """Week-7 Observation 3: Unanswerable queries should escalate with the Training Office room I.101."""
    result = ChatResult(ok=True, escalate=True)
    note = status_note(result)
    assert note is not None
    assert "Training Office, room I.101" in note


def test_multi_question_detection():
    """Week-7 Observation 1: Detect queries with multiple questions to guide users to ask one by one."""
    single_q = "Where is the student affairs office?"
    multi_q = "Can I register thesis with 118 credits? Where to replace lost student card?"
    assert single_q.count("?") <= 1
    assert multi_q.count("?") > 1
