# AI Use Log & Function Verification (Lab 8 Homework)

**Author:** HOANG GIA HUNG ([@hghung2530](https://github.com/hghung2530)) — Member 7  
**Date:** 2026-11-23  

---

## H1 — Prove it, or replace it

### 1. Function Selected
- **Function:** `parse_credits(text: str) -> tuple[int, int]` and `tuition(credits, retake, ...)` in `src/assistant_core/tools.py`.
- **Original source:** AI-assisted implementation from earlier weeks (Week 3 & Week 4) for fee calculation.

### 2. Five Edge Cases Tested (`tests/test_h1_proven_function.py`)
1. **Empty input:** `""` -> Raises `InvalidRequest("How many credits?")`.
2. **Zero credits:** `"tuition for 0 credits and 0 retake"` -> Extracted as 0, then rejected by `tuition()` with `InvalidRequest("Credits must be between 1 and 30.")`.
3. **Very large values:** `"tuition for 9999999999 credits"` -> Rejected by `tuition()` boundary check.
4. **Vietnamese language input:** `"học phí cho 18 tín chỉ và 2 học lại"` -> Correctly extracts `(18, 2)` and calculates `9,450,000 VND`.
5. **Wrong types:** Passing `None` or non-string values -> Fails fast with `TypeError` / `AttributeError`.

### 3. Bugs Discovered & Mitigations Applied
- **Issue 1:** Vietnamese queries with `"học lại"` were not parsed for retake credits.
  - *Fix:* Updated regex to `r"(\d+)\s*(?:retake|học lại)"`.
- **Issue 2:** Negative numbers (e.g. `"-5 credits"`) were stripped of the minus sign by `\d+`, converting negative inputs into valid positive credits.
  - *Fix:* Added negative prefix check `if re.search(r"-\s*\d+", text): raise InvalidRequest("Credits cannot be negative.")`.
- **Issue 3:** Numbers written as English words (e.g. `"two retakes"`) were ignored.
  - *Fix:* Added `WORD_TO_DIGIT` normalization mapping before regex extraction.

**Test outcome:** All 5 edge case tests pass (`5/5 passed` in `tests/test_h1_proven_function.py`).

---

## H2 — Reading Reflection (OWASP Top 10 for LLM Applications)

1. **Attack vector not previously thought of:** One attack vector I had not considered before reading OWASP Top 10 is **Indirect Prompt Injection (LLM01)**, where an adversary embeds hidden adversarial instructions inside external documents or synced handbook files rather than directly into the user's chat input.
2. **Defensive layer that stops it:** In our architecture, this attack is mitigated by our multi-layered defense: the **grounding check** strictly validates that citations match verified official chunks, while **deterministic tool boundaries** ensure that all business logic and calculations (such as tuition and office lookups) are executed purely in Python code rather than delegated to free-form LLM responses.
