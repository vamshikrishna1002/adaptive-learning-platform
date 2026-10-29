USE adaptive_learning_platform;


-- =====================================================
-- 1. ROW COUNTS
-- =====================================================

SELECT 'learners' AS table_name, COUNT(*) AS row_count
FROM learners

UNION ALL
SELECT 'courses', COUNT(*) FROM courses

UNION ALL
SELECT 'skills', COUNT(*) FROM skills

UNION ALL
SELECT 'skill_prerequisites', COUNT(*)
FROM skill_prerequisites

UNION ALL
SELECT 'content_items', COUNT(*)
FROM content_items

UNION ALL
SELECT 'content_skill', COUNT(*)
FROM content_skill

UNION ALL
SELECT 'attempts', COUNT(*)
FROM attempts

UNION ALL
SELECT 'assessment_results', COUNT(*)
FROM assessment_results

UNION ALL
SELECT 'mastery', COUNT(*)
FROM mastery

UNION ALL
SELECT 'recommendations', COUNT(*)
FROM recommendations

UNION ALL
SELECT 'learning_paths', COUNT(*)
FROM learning_paths;


-- =====================================================
-- 2. ATTEMPT -> LEARNER FK
-- Expected: 0
-- =====================================================

SELECT COUNT(*) AS invalid_attempt_learners
FROM attempts a
LEFT JOIN learners l
    ON a.learner_id = l.learner_id
WHERE l.learner_id IS NULL;


-- =====================================================
-- 3. ATTEMPT -> CONTENT FK
-- Expected: 0
-- =====================================================

SELECT COUNT(*) AS invalid_attempt_content
FROM attempts a
LEFT JOIN content_items c
    ON a.content_id = c.content_id
WHERE c.content_id IS NULL;


-- =====================================================
-- 4. ASSESSMENT -> ATTEMPT FK
-- Expected: 0
-- =====================================================

SELECT COUNT(*) AS invalid_assessment_attempts
FROM assessment_results ar
LEFT JOIN attempts a
    ON ar.attempt_id = a.attempt_id
WHERE a.attempt_id IS NULL;


-- =====================================================
-- 5. CONTENTSKILL -> SKILL FK
-- Expected: 0
-- =====================================================

SELECT COUNT(*) AS invalid_content_skill_skills
FROM content_skill cs
LEFT JOIN skills s
    ON cs.skill_id = s.skill_id
WHERE s.skill_id IS NULL;


-- =====================================================
-- 6. CONTENTSKILL -> CONTENT FK
-- Expected: 0
-- =====================================================

SELECT COUNT(*) AS invalid_content_skill_content
FROM content_skill cs
LEFT JOIN content_items c
    ON cs.content_id = c.content_id
WHERE c.content_id IS NULL;


-- =====================================================
-- 7. SCORE RANGE
-- Expected: 0
-- =====================================================

SELECT COUNT(*) AS invalid_scores
FROM assessment_results
WHERE score < 0
   OR score > 100;


-- =====================================================
-- 8. PASS FLAG RECONCILIATION
-- Passing score = 60
-- Expected: 0
-- =====================================================

SELECT COUNT(*) AS invalid_pass_flags
FROM assessment_results
WHERE
    (score >= 60 AND pass_flag = FALSE)
    OR
    (score < 60 AND pass_flag = TRUE);


-- =====================================================
-- 9. MASTERY RANGE
-- Expected: 0
-- =====================================================

SELECT COUNT(*) AS invalid_mastery_scores
FROM mastery
WHERE mastery_score < 0
   OR mastery_score > 1;


-- =====================================================
-- 10. DUPLICATE CONTENT-SKILL MAPPINGS
-- Expected: 0 rows
-- =====================================================

SELECT
    content_id,
    skill_id,
    COUNT(*) AS duplicate_count
FROM content_skill
GROUP BY
    content_id,
    skill_id
HAVING COUNT(*) > 1;


-- =====================================================
-- 11. RECOMMENDATION CONTENT-SKILL CONSISTENCY
-- Expected: 0
-- =====================================================

SELECT COUNT(*) AS invalid_recommendation_content
FROM recommendations r
LEFT JOIN content_skill cs
    ON r.recommended_content_id = cs.content_id
    AND r.recommended_skill_id = cs.skill_id
WHERE r.recommended_content_id IS NOT NULL
  AND cs.content_id IS NULL;


-- =====================================================
-- 12. RECOMMENDATION PREREQUISITE COMPLIANCE
-- Same-skill review paths are valid.
-- Expected: 0
-- =====================================================

SELECT COUNT(*) AS prerequisite_violations
FROM recommendations r
LEFT JOIN skill_prerequisites sp
    ON r.previous_skill_id = sp.parent_skill_id
    AND r.recommended_skill_id = sp.child_skill_id
WHERE r.previous_skill_id IS NOT NULL
  AND r.previous_skill_id <> r.recommended_skill_id
  AND sp.parent_skill_id IS NULL;


-- =====================================================
-- ATTEMPT TIMESTAMP ORDER
-- MySQL 8 window function
-- Expected: 0 rows
-- =====================================================

WITH ordered_attempts AS (
    SELECT
        attempt_id,
        learner_id,
        attempt_timestamp,

        CAST(
            SUBSTRING_INDEX(
                attempt_id,
                '-',
                -1
            ) AS UNSIGNED
        ) AS attempt_sequence,

        LAG(attempt_timestamp) OVER (
            ORDER BY
                CAST(
                    SUBSTRING_INDEX(
                        attempt_id,
                        '-',
                        -1
                    ) AS UNSIGNED
                )
        ) AS previous_timestamp

    FROM attempts
)

SELECT
    attempt_id,
    learner_id,
    attempt_timestamp,
    previous_timestamp
FROM ordered_attempts
WHERE previous_timestamp IS NOT NULL
  AND attempt_timestamp < previous_timestamp;


-- =====================================================
-- 14. SKILL DAG CYCLE DETECTION
-- MySQL 8 recursive CTE
-- Expected: 0 rows
-- =====================================================

WITH RECURSIVE skill_paths AS (

    SELECT
        parent_skill_id,
        child_skill_id,
        parent_skill_id AS start_skill,
        CONCAT(
            parent_skill_id,
            ',',
            child_skill_id
        ) AS visited_path

    FROM skill_prerequisites

    UNION ALL

    SELECT
        sp.parent_skill_id,
        sp.child_skill_id,
        paths.start_skill,

        CONCAT(
            paths.visited_path,
            ',',
            sp.child_skill_id
        )

    FROM skill_prerequisites sp

    INNER JOIN skill_paths paths
        ON sp.parent_skill_id = paths.child_skill_id

    WHERE FIND_IN_SET(
        sp.child_skill_id,
        paths.visited_path
    ) = 0
)

SELECT *
FROM skill_paths
WHERE child_skill_id = start_skill;


-- =====================================================
-- 15. REASON CODE VALIDATION
-- Expected: 0
-- =====================================================

SELECT COUNT(*) AS invalid_reason_codes
FROM recommendations
WHERE reason_code NOT IN (
    'PREREQ_MET',
    'LOW_MASTERY_REVIEW',
    'RETRY_FAILED_CONTENT',
    'COLD_START_DEFAULT'
);


-- =====================================================
-- 16. CONTENT TYPE ENUM
-- Expected: 0
-- =====================================================

SELECT COUNT(*) AS invalid_content_types
FROM content_items
WHERE content_type NOT IN (
    'VIDEO',
    'QUIZ',
    'ARTICLE',
    'LAB',
    'PROJECT'
);


-- =====================================================
-- 17. DIFFICULTY ENUM
-- Expected: 0
-- =====================================================

SELECT COUNT(*) AS invalid_difficulties
FROM content_items
WHERE difficulty NOT IN (
    'BEGINNER',
    'INTERMEDIATE',
    'ADVANCED'
);


-- =====================================================
-- 18. COLD START COUNT
-- Informational
-- =====================================================

SELECT COUNT(*) AS cold_start_recommendations
FROM recommendations
WHERE reason_code = 'COLD_START_DEFAULT';


-- =====================================================
-- 19. DIFFICULTY MATCH RATE
-- Informational
-- =====================================================

SELECT
    COUNT(*) AS total_recommendations,
    SUM(
        CASE
            WHEN difficulty_match = TRUE
            THEN 1
            ELSE 0
        END
    ) AS difficulty_matches,

    ROUND(
        100.0
        * SUM(
            CASE
                WHEN difficulty_match = TRUE
                THEN 1
                ELSE 0
            END
        )
        / NULLIF(COUNT(*), 0),
        2
    ) AS difficulty_match_percentage

FROM recommendations;