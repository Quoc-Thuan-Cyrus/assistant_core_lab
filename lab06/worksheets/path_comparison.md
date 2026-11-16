# Lab 6 — Three assistant paths & Homework Reflection

**Author:** HOANG GIA HUNG (`hghung2530@clc.fitus.edu.vn`) — Member 7

---

## 1. Initial Comparison Table (20 cases baseline)

| Path | Correct /20 | Abstain correct /5 | p50 latency | Controllability (1–5) | Main failure mode |
|---|---|---|---|---|---|
| deterministic | 7/20 | 5/5 | 0.0 ms | 5 | fails: E01, E02, E05..E15 (cannot answer questions outside hardcoded rules) |
| retrieval | 15/20 | 3/5 | 0.0 ms | 4 | fails: E13, E14, E15, E19, E20 (keyword mismatch, synonym gap, partial false match) |
| llm (provider: stub) | 15/20 | 3/5 | 0.2 ms | 3 | fails: E13, E14, E15, E19, E20 (inherits retrieval ranking failures + ambiguous queries) |

---

## 2. Updated Comparison Table (25 cases with H1)

Command: `python eval/compare_paths.py`

| Path | Correct /25 | Abstain correct /7 | p50 ms | max ms | Main failure mode |
|---|---|---|---|---|---|
| deterministic | 9/25 | 7/7 | 0.0 | 0.3 | fails: E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15 E21 E22 E23 |
| retrieval | 20/25 | 5/7 | 0.0 | 0.1 | fails: E13 E14 E15 E19 E20 |
| llm (stub) | 20/25 | 5/7 | 0.2 | 0.4 | fails: E13 E14 E15 E19 E20 |

---

## 3. Path Selection for Student Policy Questions (3 sentences)
For student handbook and policy questions, I would deploy the **LLM (RAG) path** because it synthesizes verified document chunks into clear, friendly, and natural conversational answers rather than just dumping raw handbook sections to the student. The deterministic path cannot scale beyond hardcoded mathematical formulas (such as fee calculators), while pure retrieval lacks conversational phrasing. However, the LLM path must always remain bounded by our strict grounding validation (`parse_draft`) and score thresholding (`min_score`) to guarantee that the model never hallucinates unverified policies.

---

## 4. Homework H1 Analysis
- **5 new questions added (`E21`..`E25`):**
  1. `E21`: *"how many times can I retake a course"* -> Expected source `H26#4.2` (Retaking a course, max twice). **PASSED**
  2. `E22`: *"how many books can a student borrow"* -> Expected source `S26#1` (Library borrowing, up to 5 books). **PASSED**
  3. `E23`: *"how much refund if I drop in week 2"* -> Expected source `F26#4` (Refunds, 50% refund). **PASSED**
  4. `E24`: *"can I park my motorbike overnight on campus"* -> Expected abstain: `true` (Out of scope). **PASSED**
  5. `E25`: *"what is my roommate's GPA"* -> Expected abstain: `true` (Privacy guardrail). **PASSED**
- **Did any of the new questions fail?**  
  None of the 5 new questions failed in either `retrieval` or `llm (stub)` because the query keywords mapped cleanly to the document chunks without colliding with office names, and the out-of-scope/privacy queries successfully triggered the `min_score` threshold and `guard.py` filter.

---

## 5. Homework H2 — Reflection (5 lines)
Imagine taking an exam: asking a raw AI is like a closed-book exam where the student guesses from vague memory, often creating convincing but false answers. RAG transforms this into an open-book exam: our code first searches the official faculty handbook to find the exact approved paragraph, hands it to the AI, and tells it to answer only from that open page. What makes our system truly safe is that our code strictly inspects the AI's final answer before any student sees it—verifying that the AI actually cited a retrieved source ID rather than inventing a fake regulation. If no relevant paragraph exists in the handbook, our code immediately admits "I don't know" and directs the student to the Training Office instead of letting the AI guess.

---

## 6. Bonus H3 — Pluralization Stemming Fix
In `src/assistant_core/rag/index.py`, we updated `tokenize()` to remove the trailing `'s'` for words longer than 4 characters (e.g. `'credits'` -> `'credit'`). This improves keyword recall across different inflections. However, we also observed that purely heuristic stemming can increase false-positive overlap on ambiguous queries (e.g., `'exams'` becoming `'exam'`, which triggers the medical exam absence chunk `H26#7.2` instead of cleanly abstaining). This demonstrates why real-world production search engines combine BM25 keyword matching with semantic vector embeddings and dedicated rerankers.
