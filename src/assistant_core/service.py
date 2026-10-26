import logging

from assistant_core.errors import InvalidRequest, ProviderError
from assistant_core.models import Intent, Message, Response, Source
from assistant_core.responder import TemplateResponder
from assistant_core.router import route
from assistant_core.tools import parse_credits, tuition  # Import thêm công cụ tính toán

# Lưu ý: Cần import thêm hàm _fee từ tools nếu bạn tách nó ra,
# ở đây tài liệu dùng self._fee() như một phương thức nội bộ hoặc gọi trực tiếp tools.tuition().

log = logging.getLogger(__name__)


class AssistantService:
    def __init__(self, settings, offices, handbook, responder):
        self.settings, self.offices, self.handbook = settings, offices, handbook
        self.responder = responder
        self.fallback = TemplateResponder()

    def handle(self, msg: Message) -> Response:
        intent = route(msg.text, self.offices.names)
        if intent is Intent.GREETING:
            return Response(answer="Hello! I can help with offices, fees and rules.", intent=intent)
        if intent is Intent.FEE:
            return self._fee(msg.text)  # Giả định bạn đã bọc tools.tuition vào hàm _fee
        if intent is Intent.OFFICE:
            o = self.offices.find(msg.text)
            return Response(answer=f"{o.name}: room {o.room}, open {o.hours}.", intent=intent)
        return self._rule(msg.text)

    def _rule(self, text: str) -> Response:
        rule = self.handbook.search(text)
        if rule is None:
            return Response(answer="Sorry, I don't know that yet.", intent=Intent.UNKNOWN)
        sources = [Source(id=rule.id, title=rule.title)]
        try:
            return Response(answer=self.responder.explain(text, rule), intent=Intent.RULE, sources=sources)
        except ProviderError:
            log.warning("provider failed; using template fallback")
            answer = self.fallback.explain(text, rule)
            return Response(answer=answer, intent=Intent.RULE, sources=sources, degraded=True)

    def _fee(self, text: str) -> Response:
        # Remove the try...except block so the InvalidRequest error is raised
        credits, retake = parse_credits(text)
        
        cost = tuition(
            credits,
            retake,
            self.settings.credit_rate_vnd,
            self.settings.retake_multiplier,
            self.settings.max_credits,
        )
        return Response(answer=f"Your tuition is {cost:,} VND.", intent=Intent.FEE)
