# Lab 7 homework — 10-minute usability test

Tester (not in your team, first name only): Nam  Date: 2026-11-23
Task you gave them: "Find out if you can register your thesis with 118 credits, and where to replace a lost student card."

Rule: do not help or explain. Watch and write down what happens.

| # | What the tester did or said | What they expected | Why the system/UI caused it | Fix idea |
|---|---|---|---|---|
| 1 | Entered both questions together in one prompt: *"Can I register my thesis with 118 credits, and where to replace a lost student card?"* | Expected the assistant to answer both questions in a structured multi-part response. | The chat input placeholder was generic (`"Ask about fees, offices or the handbook…"`), not indicating single-turn intent limitations. The RAG system retrieved only thesis chunks and completely missed the student card question. | Change placeholder to explicitly prompt for one question at a time, and add proactive hint detection when multiple questions (`? > 1`) are entered. |
| 2 | Clicked repeatedly on the source identifier `H26#5.3`, asking *"Can I click this to read the actual paragraph?"* | Expected an interactive link or popup showing the exact text excerpt from handbook section 5.3. | Sources were rendered as flat static text (`Sources: H26#5.3 — 5.3 Thesis registration`) without visual depth or expandability. | Group sources inside an interactive `st.expander("📚 Sources (N)")` with distinct bold badges for chunk IDs. |
| 3 | Asked *"Where can I get a student bus pass?"*, received escalation note: *"Training Office, room I.101"*, then asked *"Is room I.101 open right now or can I email them?"* | Expected opening hours and contact channels (email/hotline) alongside room location. | The escalation fallback in `logic.py` only provides physical room number without operational hours or alternative contact channels. | Include operating hours (e.g. 7:30–11:30, 13:30–16:30) and department contact email in the escalation note. |

The one change we made:
- Added multi-question guidance in `ui/app.py`:
  1. Updated `st.chat_input` placeholder to `"Ask one question at a time (fees, offices, or the handbook)…"`.
  2. Added proactive detection when `question.count("?") > 1` to show a user-friendly tip: *"Tip: It looks like you asked multiple questions at once. Try asking one question at a time for a complete answer."*

Before / after screenshot:
- **Before (`image.png`)**: Ambiguous input placeholder, tester submits multi-question prompt without guidance.
- **After (`image-1.png`)**: Clear placeholder guidance and proactive multi-question tip rendered under the answer.

---

## H2 — Reading Reflection (Google PAIR Guidebook)
**Readings:** *Feedback + Control* and *Errors + Graceful Failure*

1. **Idea used today:** We implemented graceful failure by having the assistant abstain and provide a concrete human escalation path (the Training Office in room I.101) when official documentation is insufficient, combined with explicit user control through 👍/👎 feedback buttons with immediate acknowledgment toasts.
2. **Idea to add in the future:** We would incorporate PAIR's recommendation of progressive disclosure with interactive suggestion chips for ambiguous queries, allowing users to disambiguate their intent before a failure occurs rather than falling back directly to an escalation note.
