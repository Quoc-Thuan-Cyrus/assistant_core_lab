-- Lab 5 Part F & H2: Queries for the assistant database
-- Database: assistant.db (seeded with scripts/seed.py)

-- ============================================================================
-- F1: How many questions per intent?
-- ============================================================================
SELECT intent, COUNT(*) AS requests 
FROM interaction 
GROUP BY intent 
ORDER BY requests DESC;

/* Result:
intent     | requests
-----------+---------
rule       | 280
fee        | 122
office     | 94
greeting   | 52
unknown    | 52
*/

-- ============================================================================
-- F2: Average time taken per intent (ms)?
-- ============================================================================
SELECT intent, ROUND(AVG(latency_ms), 1) AS avg_latency_ms 
FROM interaction 
GROUP BY intent 
ORDER BY avg_latency_ms DESC;

/* Result:
intent     | avg_latency_ms
-----------+---------------
rule       | 76.2
unknown    | 8.1
fee        | 5.1
office     | 3.4
greeting   | 2.4
*/

-- ============================================================================
-- F3: Which topics got the most thumbs-down?
-- ============================================================================
SELECT i.topic, COUNT(*) AS thumbs_down 
FROM interaction i 
JOIN feedback f ON f.request_id = i.request_id 
WHERE f.rating = -1 
GROUP BY i.topic 
ORDER BY thumbs_down DESC;

/* Result:
topic      | thumbs_down
-----------+------------
NULL       | 34
H26-5.3    | 16
H26-4.2    | 16
H26-7.2    | 4
*/

-- ============================================================================
-- H2: One question about the assistant data (Product Question)
-- Question 1: "Which hour of the day is the busiest?"
-- ============================================================================
SELECT strftime('%H', created_at) AS hour, COUNT(*) AS requests 
FROM interaction 
GROUP BY hour 
ORDER BY requests DESC;

/* Result:
hour       | requests
-----------+---------
07         | 600
*/

-- ============================================================================
-- H2 Bonus: "What share of answers used a backup path (degraded responses)?"
-- ============================================================================
SELECT ROUND(100.0 * SUM(CASE WHEN degraded THEN 1 ELSE 0 END) / COUNT(*), 2) AS degraded_percentage 
FROM interaction;

/* Result:
degraded_percentage
-------------------
12.67
*/
