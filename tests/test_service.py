import pytest  # type: ignore
from assistant_core.errors import InvalidRequest  # type: ignore
from assistant_core.models import Intent, Message  # type: ignore
from assistant_core.responder import StubLLMResponder  # type: ignore
from pydantic import ValidationError  # type: ignore

from unittest.mock import MagicMock
import pytest # type: ignore
from assistant_core.responder import StubLLMResponder # type: ignore

# Import your service (adjust the import path if it's in assistant_core.service)
from assistant_core.service import AssistantService
@pytest.fixture
def service():
    # 1. Setup mock settings for the fee calculation
    settings = MagicMock()
    settings.credit_rate_vnd = 450000       # adjust to match your math
    settings.retake_multiplier = 1.5        # adjust to match your math
    settings.max_credits = 24               # adjust as needed
    
    # 2. Setup mock offices for the office lookup
    offices = MagicMock()
    offices.names = ["academic affairs"]
    mock_office = MagicMock()
    mock_office.name = "Academic Affairs"
    mock_office.room = "E102"
    mock_office.hours = "8AM-5PM"
    offices.find.return_value = mock_office
    
    # 3. Setup mock handbook for rule lookup
    handbook = MagicMock()
    mock_rule = MagicMock()
    mock_rule.id = "R01"
    mock_rule.title = "Thesis Registration"
    # Ensure handbook.search returns the mock rule for the known query, and None otherwise
    handbook.search.side_effect = lambda text: mock_rule if "thesis" in text.lower() else None
    
    # 4. Setup the responder
    responder = StubLLMResponder(fail=False)
    
    # Return the initialized service
    return AssistantService(settings, offices, handbook, responder)
def test_greeting_response(service):
    r = service.handle(Message(text="Hello!"))
    assert r.intent is Intent.GREETING
    assert "Hello!" in r.answer
    assert not r.degraded


def test_fee_calculation_response(service):
    r = service.handle(Message(text="tuition for 18 credits and 2 retake"))
    assert r.intent is Intent.FEE
    assert "9,450,000" in r.answer or "9450000" in r.answer
    assert not r.degraded


def test_fee_invalid_credits_raises(service):
    with pytest.raises(InvalidRequest):
        service.handle(Message(text="tuition for 0 credits"))


def test_office_lookup_response(service):
    r = service.handle(Message(text="Where is academic affairs?"))
    assert r.intent is Intent.OFFICE
    assert "E102" in r.answer
    assert not r.degraded


def test_rule_lookup_normal_response(service):
    r = service.handle(Message(text="thesis registration credits"))
    assert r.intent is Intent.RULE
    assert not r.degraded
    assert len(r.sources) == 1
    assert r.sources[0].id == "R01"


def test_fallback_when_provider_fails(service):
    service.responder = StubLLMResponder(fail=True)
    r = service.handle(Message(text="thesis registration credits"))
    assert r.intent is Intent.RULE
    assert r.degraded
    assert len(r.sources) == 1
    assert "Thesis Registration" in r.answer


def test_unknown_rule_response(service):
    r = service.handle(Message(text="quantum physics laboratory schedule"))
    assert r.intent is Intent.UNKNOWN
    assert not r.degraded
    assert r.sources == []


def test_empty_message_rejected_by_pydantic():
    with pytest.raises(ValidationError):
        Message(text="")
