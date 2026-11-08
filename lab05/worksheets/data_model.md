# Lab 5 — Data model worksheet

## 1. Critique the bad schema (sql/bad_schema.sql)
| # | Problem | Why it hurts | Fix |
|---|---|---|---|
| 1 |Storing student_name and student_phone |Creates severe privacy risks and violates data protection laws by storing unneeded personal data |Remove these columns entirely |
| 2 |Storing the full raw message |The raw text may contain personal details, creating a leak risk |Store only the categorized intent and topic metadata |
| 3 |feedback stored as a comma-separated text list (e.g., '1,-1,1') |impossible to query, count, or link specific ratings to specific responses using SQL |Create a separate feedback table linked by a foreign key |
| 4 |id is just an INTEGER without being marked as a primary key |database won't enforce uniqueness, allowing duplicate IDs |Define it as INTEGER PRIMARY KEY |
| 5 |time is stored as a formatted TEXT string |cannot easily sort by date or calculate time differences |Use a standard DATETIME format |
| 6 |latency is stored as text |cannot calculate the average or sum of text fields |Store it as a numeric FLOAT or INTEGER representing milliseconds |

## 2. Store or not? (privacy-aware storage)
| Data | Store? | Form (raw / hashed / aggregated / none) | Retention | Reason |
|---|---|---|---|---|
| raw user message |no |none | |May contain personal details |
| session id |yes |hashed |allows count sessions without knowing who | |
| intent, latency, topic |yes |raw | |Tells us what to improve |
| feedback rating |Yes |raw | |allows for real feedback |
| feedback comment |Yes |raw |   |allows for real feedback |
| student name / phone |No |none | |No feature needs it |

## 3. Product questions → fields
| Product question | Fields needed | Table(s) | Query sketch |
|---|---|---|---|
| Most failed intent? |intent, resolved |interaction |SELECT intent, COUNT(*) FROM interaction WHERE resolved = False GROUP BY intent ORDER BY COUNT(*) DESC; |
| Average response time by intent? |intent, latency_ms |interaction |SELECT intent, ROUND(AVG(latency_ms), 1) FROM interaction GROUP BY intent; |
| Top unresolved topics? |topic, resolved |interaction |SELECT topic, COUNT(*) FROM interaction WHERE resolved = False GROUP BY topic ORDER BY COUNT(*) DESC; |

## 4. ER diagram
Draw entities, keys and relationships (photo or Mermaid in docs/data-model.md).
erDiagram
    chat_session ||--o{ interaction : "1:N"
    interaction ||--o{ feedback : "1:N"

    chat_session {
        string id PK "salted hash"
        string channel
        datetime created_at
    }
    interaction {
        int id PK
        string request_id UQ
        string session_id FK
        string intent
        string topic
        boolean resolved
        boolean degraded
        float latency_ms
        datetime created_at
    }
    feedback {
        int id PK
        string request_id FK
        int rating "-1/0/1"
        string comment
        datetime created_at
    }