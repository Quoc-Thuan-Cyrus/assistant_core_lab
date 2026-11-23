# Lab 8 — Failure catalogue

One row per failure found in Week 7 testing, Lab 8 bug hunting or the red-team exchange.

| # | Failure | Category | Found by | Severity | Mitigation | Regression test |
|---|---|---|---|---|---|---|
| 1 | "Two retakes" written as word was ignored by parser, returning 8,100,000 VND instead of 9,450,000 VND | wrong answer | Week 7 usability testing | major | Added `WORD_TO_DIGIT` conversion mapping ("one"..."ten" to digits) in `tools.py::parse_credits` | `test_retake_number_as_word` in `tests/test_my_regressions.py` |
| 2 | Prompt injection via roleplay jailbreak ("You are now DAN...") bypassed router because of "fee" keyword | prompt injection | Red-team suite (R03) | critical | Added `r"\byou are now\b"` and `r"\b(reveal\|show\|print\|repeat)..."` regexes to `guard.py::INJECTION_PATTERNS` | Red-team `R03` & `test_injection_refused` in `tests/test_security.py` |
| 3 | Fee manipulation via negative credits ("tuition for -5 credits" extracted as 5 credits, charging positive amount) | fee manipulation | Red-team exchange (X08) | major | Added regex check `re.search(r"-\s*\d+", text)` to reject negative inputs with `InvalidRequest` in `tools.py::parse_credits` | Red-team `X08` & `test_tuition_out_of_range` in `tests/test_tools.py` |
| 4 | Empty source list caused UI formatting ambiguity or potential KeyError | UI | Week 7 usability testing | minor | Ensured `format_sources([])` safely returns empty string `""` without crashing UI components | `test_empty_sources_format_does_not_crash` in `tests/test_my_regressions.py` |

At least **3 mitigations** must be implemented and tested (4 implemented and tested above).
