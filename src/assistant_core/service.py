import logging
from pathlib import Path

from assistant_core.config import load_settings
from assistant_core.errors import ProviderError
from assistant_core.knowledge import Handbook, OfficeDirectory
from assistant_core.models import Intent, Message, Response, Source
from assistant_core.responder import TemplateResponder
from assistant_core.router import route
from assistant_core.tools import parse_credits, tuition

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
            return self._fee(msg.text)
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
        credits, retake = parse_credits(text)
        cost = tuition(
            credits,
            retake,
            self.settings.credit_rate_vnd,
            self.settings.retake_multiplier,
            self.settings.max_credits,
        )
        return Response(answer=f"Your tuition is {cost:,} VND.", intent=Intent.FEE)


def build_service(settings=None):
    settings = settings or load_settings()
    data_dir = settings.data_dir
    offices_csv = data_dir / "offices.csv"
    handbook_json = data_dir / "handbook.json"

    # Fallback to repo root data directory if not found in current working directory
    if not offices_csv.is_file():
        default_data = Path(__file__).resolve().parents[2] / "data"
        if (default_data / "offices.csv").is_file():
            data_dir = default_data
            offices_csv = data_dir / "offices.csv"
            handbook_json = data_dir / "handbook.json"

    return AssistantService(
        settings=settings,
        offices=OfficeDirectory.from_csv(offices_csv),
        handbook=Handbook.from_json(handbook_json),
        responder=TemplateResponder(),
    )
