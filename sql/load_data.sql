USE adaptive_learning_platform;

-- =====================================================
-- CLEAR EXISTING DATA
-- =====================================================

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE learning_paths;
TRUNCATE TABLE recommendations;
TRUNCATE TABLE mastery;
TRUNCATE TABLE assessment_results;
TRUNCATE TABLE attempts;
TRUNCATE TABLE content_skill;
TRUNCATE TABLE skill_prerequisites;
TRUNCATE TABLE content_items;
TRUNCATE TABLE skills;
TRUNCATE TABLE courses;
TRUNCATE TABLE learners;

SET FOREIGN_KEY_CHECKS = 1;


-- =====================================================
-- 1. LEARNERS
-- =====================================================

LOAD DATA LOCAL INFILE
'C:/Users/akula/OneDrive/Desktop/adaptive-learning-platform/data/output/learners.csv'
INTO TABLE learners
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    learner_id,
    learner_status,
    @registration_date
)
SET
    registration_date = TRIM(TRAILING '\r' FROM @registration_date);


-- =====================================================
-- 2. COURSES
-- =====================================================

LOAD DATA LOCAL INFILE
'C:/Users/akula/OneDrive/Desktop/adaptive-learning-platform/data/output/courses.csv'
INTO TABLE courses
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    course_id,
    course_name,
    @course_category
)
SET
    course_category = TRIM(TRAILING '\r' FROM @course_category);


-- =====================================================
-- 3. SKILLS
-- =====================================================

LOAD DATA LOCAL INFILE
'C:/Users/akula/OneDrive/Desktop/adaptive-learning-platform/data/output/skills.csv'
INTO TABLE skills
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    skill_id,
    @skill_name
)
SET
    skill_name = TRIM(TRAILING '\r' FROM @skill_name);


-- =====================================================
-- 4. SKILL PREREQUISITES
-- =====================================================

LOAD DATA LOCAL INFILE
'C:/Users/akula/OneDrive/Desktop/adaptive-learning-platform/data/output/skill_prerequisites.csv'
INTO TABLE skill_prerequisites
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    parent_skill_id,
    @child_skill_id
)
SET
    child_skill_id = TRIM(TRAILING '\r' FROM @child_skill_id);


-- =====================================================
-- 5. CONTENT ITEMS
-- =====================================================

LOAD DATA LOCAL INFILE
'C:/Users/akula/OneDrive/Desktop/adaptive-learning-platform/data/output/content_items.csv'
INTO TABLE content_items
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    content_id,
    content_title,
    content_type,
    @difficulty
)
SET
    difficulty = TRIM(TRAILING '\r' FROM @difficulty);


-- =====================================================
-- 6. CONTENT-SKILL MAPPING
-- =====================================================

LOAD DATA LOCAL INFILE
'C:/Users/akula/OneDrive/Desktop/adaptive-learning-platform/data/output/content_skill.csv'
INTO TABLE content_skill
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    content_id,
    @skill_id
)
SET
    skill_id = TRIM(TRAILING '\r' FROM @skill_id);


-- =====================================================
-- 7. ATTEMPTS
-- =====================================================

LOAD DATA LOCAL INFILE
'C:/Users/akula/OneDrive/Desktop/adaptive-learning-platform/data/output/attempts.csv'
INTO TABLE attempts
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    attempt_id,
    learner_id,
    content_id,
    @attempt_timestamp
)
SET
    attempt_timestamp =
        TRIM(TRAILING '\r' FROM @attempt_timestamp);


-- =====================================================
-- 8. ASSESSMENT RESULTS
-- =====================================================

LOAD DATA LOCAL INFILE
'C:/Users/akula/OneDrive/Desktop/adaptive-learning-platform/data/output/assessment_results.csv'
INTO TABLE assessment_results
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    attempt_id,
    learner_id,
    content_id,
    score,
    pass_flag,
    @attempt_timestamp
)
SET
    attempt_timestamp =
        TRIM(TRAILING '\r' FROM @attempt_timestamp);


-- =====================================================
-- 9. MASTERY
-- =====================================================

LOAD DATA LOCAL INFILE
'C:/Users/akula/OneDrive/Desktop/adaptive-learning-platform/data/output/mastery.csv'
INTO TABLE mastery
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    learner_id,
    skill_id,
    mastery_score,
    @mastery_as_of_timestamp
)
SET
    mastery_as_of_timestamp =
        TRIM(
            TRAILING '\r'
            FROM @mastery_as_of_timestamp
        );


-- =====================================================
-- 10. RECOMMENDATIONS
-- =====================================================

LOAD DATA LOCAL INFILE
'C:/Users/akula/OneDrive/Desktop/adaptive-learning-platform/data/output/recommendations.csv'
INTO TABLE recommendations
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    learner_id,
    @previous_skill_id,
    recommended_skill_id,
    recommended_content_id,
    reason_code,
    target_difficulty,
    recommended_difficulty,
    difficulty_rank,
    @difficulty_match
)
SET
    previous_skill_id =
        NULLIF(
            TRIM(@previous_skill_id),
            ''
        ),

    difficulty_match =
        CASE
            WHEN TRIM(
                TRAILING '\r'
                FROM @difficulty_match
            ) IN ('True', 'TRUE', '1')
            THEN 1

            WHEN TRIM(
                TRAILING '\r'
                FROM @difficulty_match
            ) IN ('False', 'FALSE', '0')
            THEN 0

            ELSE NULL
        END;


-- =====================================================
-- 11. LEARNING PATHS
-- =====================================================

LOAD DATA LOCAL INFILE
'C:/Users/akula/OneDrive/Desktop/adaptive-learning-platform/data/output/learning_paths.csv'
INTO TABLE learning_paths
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    path_id,
    learner_id,
    current_skill_id,
    @previous_skill_id
)
SET
    previous_skill_id =
        NULLIF(
            TRIM(
                TRAILING '\r'
                FROM @previous_skill_id
            ),
            ''
        );


-- =====================================================
-- LOAD VERIFICATION
-- =====================================================

SELECT 'learners' AS table_name, COUNT(*) AS row_count
FROM learners

UNION ALL
SELECT 'courses', COUNT(*)
FROM courses

UNION ALL
SELECT 'skills', COUNT(*)
FROM skills

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