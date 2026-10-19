from assistant_core.models import Message
from assistant_core.responder import StubLLMResponder


def test_fallback_when_provider_fails(service):  # service ở đây là một fixture bạn tự định nghĩa trong conftest.py
    service.responder = StubLLMResponder(fail=True)
    r = service.handle(Message(text="thesis registration credits"))
    assert r.degraded and r.sources
