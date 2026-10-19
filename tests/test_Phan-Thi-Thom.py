from assistant_core.errors import AssistantError, ConfigError
from assistant_core.models import Intent, Message, Response


def test_errors():
    err = ConfigError("Thiếu file cấu hình")
    assert isinstance(err, AssistantError)


def test_models():
    msg = Message(text="Xin chào")
    assert msg.text == "Xin chào"
    assert msg.session_id == "local"

    res = Response(answer="Chào bạn!", intent=Intent.GREETING)
    assert res.intent == Intent.GREETING
    assert res.answer == "Chào bạn!"