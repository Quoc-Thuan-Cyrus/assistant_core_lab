"""Homework H1: Prove (or replace) one AI-generated function with tests.

Function under test: assistant_core.tools.parse_credits and assistant_core.tools.tuition
Five edge cases: empty input, zero, very large values, Vietnamese text, wrong types.
"""

import pytest

from assistant_core.errors import InvalidRequest
from assistant_core.tools import parse_credits, tuition


def test_h1_empty_input():
    """Edge case 1: Empty input must raise InvalidRequest."""
    with pytest.raises(InvalidRequest, match="How many credits"):
        parse_credits("")


def test_h1_zero_credits():
    """Edge case 2: Zero credits must be rejected by tuition calculation."""
    credits, retake = parse_credits("tuition for 0 credits and 0 retake")
    assert credits == 0
    with pytest.raises(InvalidRequest, match="Credits must be between 1 and 30"):
        tuition(credits, retake, 450_000, 1.5, 30)


def test_h1_very_large_values():
    """Edge case 3: Very large credit counts must be rejected."""
    credits, retake = parse_credits("tuition for 9999999999 credits")
    assert credits == 9999999999
    with pytest.raises(InvalidRequest, match="Credits must be between 1 and 30"):
        tuition(credits, retake, 450_000, 1.5, 30)


def test_h1_vietnamese_text():
    """Edge case 4: Vietnamese query 'học phí cho 18 tín chỉ và 2 học lại' must parse correctly."""
    credits, retake = parse_credits("học phí cho 18 tín chỉ và 2 học lại")
    assert credits == 18
    assert retake == 2
    assert tuition(credits, retake, 450_000, 1.5, 30) == 9_450_000


def test_h1_wrong_types():
    """Edge case 5: Passing non-string inputs (None, int, list) must raise an appropriate error."""
    with pytest.raises((TypeError, AttributeError)):
        parse_credits(None)  # type: ignore[arg-type]
    with pytest.raises((TypeError, AttributeError)):
        parse_credits(12345)  # type: ignore[arg-type]
