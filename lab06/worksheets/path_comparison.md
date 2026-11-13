# Lab 6 — Three assistant paths

Run `python eval/compare_paths.py` and fill in.

| Path                 | Correct /20 | Abstain correct /5 | p50 latency | Controllability (1–5) | Main failure mode |
|---                   |---|---|---  |---                 |---|
| deterministic        | 7/ 20 | 5/5 | 0.0|0.4  |fails: E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15 |
| retrieval            |16/20  | 4/5 | 0.0|0.1  |fails: E13 E14 E15 E19 |
| llm (provider: ____) |16/20 |4/5 |0.2 |0.5 |fails: E13 E14 E15 E19 |

Which path would you ship for policy questions, and why? (3 sentences)
 I would use the LLM path for student handbook questions because it can synthesize the rules from the retrieved paragraphs into a friendly, clear answer rather than just pasting raw text. The deterministic path is only suited for strict rule-based logic like calculating fees, so it cannot handle general policy questions. I would prioritize fixing case E14 first, because a search engine should easily recognize that "credit" and "credits" are the same word without failing to find the right document.   