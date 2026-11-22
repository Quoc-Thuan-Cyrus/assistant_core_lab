# Lab 6 homework — five difficult queries

Force 5 difficult or ambiguous queries. The assistant must **abstain or escalate** instead of inventing an answer.

| # | Query | Category (ambiguous / out-of-scope / privacy / not in docs / conflicting) | Before: path + answer | Fix you made | After: path + answer |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

Add all five to `eval/cases.jsonl` with `"expect_abstain": true` and show the new comparison table.
path                correct  abstain ok  p50 ms  max ms
deterministic          9/25       7/7     0.0     0.4   fails: E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15 E21 E22 E23
retrieval             20/25       6/7     0.0     0.1   fails: E13 E14 E15 E19 E23
llm (stub)            20/25       6/7     0.3     0.9   fails: E13 E14 E15 E19 E23
## Case E23 failed because the student asked when registration will "close", but the document uses the word "closes", which our simple word-matching search engine treats as a completely different word.

## H2 Reflection
RAG is like giving an AI an open-book exam instead of a closed-book one where it has to guess from memory. First, our search engine finds the exact paragraph in our official rulebook that contains the answer. Then, we hand that specific paragraph to the AI and tell it to write a friendly response using only that text. To make sure the AI doesn't invent rules, our code performs a "grounding check" to verify that the AI only cites the exact source paragraph we provided. If the search engine finds nothing, our code forces the system to say "I don't know" before the AI even gets a chance to guess.   

## H3 bonus
Case E14 now passes because "credits" is stripped down to "credit", allowing it to match the handbook text. Additionally, my custom case E23 ("when does thesis registration close") also started passing, because the handbook's word "closes" was stripped down to "close", successfully matching my query.