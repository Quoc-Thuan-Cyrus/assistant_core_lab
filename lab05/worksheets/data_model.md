# Lab 5 — Data model worksheet

## 1. Critique the bad schema (sql/bad_schema.sql)
| # | Problem | Why it hurts | Fix |
|---|---|---|---|
| 1 | Storing `student_name` and `student_phone` | Creates severe privacy risks and violates data protection regulations (e.g., Vietnam Personal Data Protection Decree) by storing unneeded personal data | Remove these columns entirely |
| 2 | Storing full raw `message` | Raw user queries can contain sensitive personal identifiable info (PII) | Store only structured metadata (intent, topic) instead of raw text |
| 3 | `feedback` stored as a comma-separated text list (e.g. `'1,-1,1'`) | Violates 1NF; cannot easily query, index, aggregate, or link ratings to specific responses | Create a dedicated `feedback` table linked to `interaction` via foreign key `request_id` |
| 4 | `id` is an untyped INTEGER without `PRIMARY KEY` | The database does not enforce row uniqueness or create an automatic index | Define as `INTEGER PRIMARY KEY` (or `AUTOINCREMENT`) |
| 5 | `time` is stored as free-form formatted TEXT (e.g. `'5/10/2026 9:03 PM'`) | Cannot reliably sort chronologically, filter by date ranges, or compute intervals | Use standard ISO-8601 UTC `TIMESTAMP` |
| 6 | `latency` is stored as text (e.g. `'120ms'`) | Cannot calculate mathematical aggregations like `AVG()`, `MAX()`, `MIN()` directly in SQL | Store as numeric `FLOAT` or `INTEGER` representing milliseconds |

## 2. Store or not? (privacy-aware storage)
| Data | Store? | Form (raw / hashed / aggregated / none) | Retention | Reason |
|---|---|---|---|---|
| raw user message | no | none | 0 days | May contain personal details / PII; no operational need |
| session id | yes | hashed | 90 days | Allows counting unique sessions while preserving privacy |
| intent, latency, topic | yes | raw | 1 year | Analyzes system usage, performance, and trends |
| feedback rating | yes | raw | 1 year | Evaluates satisfaction and tracks quality over time |
| feedback comment | yes | raw | 90 days | Identifies user complaints and actionable suggestions |
| student name / phone | no | none | 0 days | Not needed for assistant functionality; high privacy risk |

## 3. Product questions → fields
| Product question | Fields needed | Table(s) | Query sketch |
|---|---|---|---|
| Most failed intent? | `intent`, `resolved` | `interaction` | `SELECT intent, COUNT(*) FROM interaction WHERE resolved = 0 GROUP BY intent ORDER BY COUNT(*) DESC;` |
| Average response time by intent? | `intent`, `latency_ms` | `interaction` | `SELECT intent, ROUND(AVG(latency_ms), 1) AS avg_ms FROM interaction GROUP BY intent;` |
| Top unresolved topics? | `topic`, `resolved` | `interaction` | `SELECT topic, COUNT(*) FROM interaction WHERE resolved = 0 GROUP BY topic ORDER BY COUNT(*) DESC;` |

## 4. ER diagram
Draw entities, keys and relationships (photo or Mermaid in docs/data-model.md).

```mermaid
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
```
