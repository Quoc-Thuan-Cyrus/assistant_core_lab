"""HTTP request/response schemas — the public API contract (v1)."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from assistant_core.models import Intent, Source
from typing import Literal
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000, examples=["tuition for 18 credits and 2 retake"])
    session_id: str = Field(default="anonymous", max_length=64)


class ChatResponse(BaseModel):
    answer: str
    intent: Intent
    sources: list[Source] = []
    degraded: bool = False
    request_id: str


class FeedbackIn(BaseModel):
    request_id: str
    rating: Literal[-1, 0, 1]
    comment: str | None = None

class FeedbackOut(FeedbackIn):
    id: int
    created_at: datetime


class Weather(BaseModel):
    temperature_c: float
    wind_kmh: float
    description: str
    observed_at: str
    stale: bool = False  # True when served from cache after an upstream failure


class ErrorBody(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorBody
