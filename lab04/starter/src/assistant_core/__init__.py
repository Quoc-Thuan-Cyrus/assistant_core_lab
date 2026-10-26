"""assistant_core — the service layer of the CSC10014 study assistant."""

from assistant_core.models import Message, Response
from assistant_core.service import AssistantService, build_service
from .service import AssistantService, build_service
from .models import Message  # (Or .schemas, depending on your Lab 3 file structure)

__all__ = ["AssistantService", "Message", "Response", "build_service"]
