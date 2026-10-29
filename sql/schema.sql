CREATE DATABASE IF NOT EXISTS adaptive_learning_platform
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE adaptive_learning_platform;


-- =====================================================
-- 1. LEARNERS
-- =====================================================

CREATE TABLE learners (
    learner_id VARCHAR(20) PRIMARY KEY,
    learner_status VARCHAR(20) NOT NULL,
    registration_date DATE NOT NULL,

    CONSTRAINT chk_learner_status
        CHECK (
            learner_status IN (
                'REGISTERED',
                'ACTIVE',
                'INACTIVE',
                'SUSPENDED'
            )
        )
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;


-- =====================================================
-- 2. COURSES
-- =====================================================

CREATE TABLE courses (
    course_id VARCHAR(20) PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    course_category VARCHAR(100) NOT NULL
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;


-- =====================================================
-- 3. SKILLS
-- =====================================================

CREATE TABLE skills (
    skill_id VARCHAR(20) PRIMARY KEY,
    skill_name VARCHAR(255) NOT NULL
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;


-- =====================================================
-- 4. SKILL PREREQUISITES
-- =====================================================

CREATE TABLE skill_prerequisites (
    parent_skill_id VARCHAR(20) NOT NULL,
    child_skill_id VARCHAR(20) NOT NULL,

    PRIMARY KEY (
        parent_skill_id,
        child_skill_id
    ),

    CONSTRAINT fk_skill_prereq_parent
        FOREIGN KEY (parent_skill_id)
        REFERENCES skills(skill_id),

    CONSTRAINT fk_skill_prereq_child
        FOREIGN KEY (child_skill_id)
        REFERENCES skills(skill_id),

    CONSTRAINT chk_no_self_prerequisite
        CHECK (
            parent_skill_id <> child_skill_id
        )
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;


-- =====================================================
-- 5. CONTENT ITEMS
-- =====================================================

CREATE TABLE content_items (
    content_id VARCHAR(20) PRIMARY KEY,
    content_title VARCHAR(255) NOT NULL,
    content_type VARCHAR(30) NOT NULL,
    difficulty VARCHAR(30) NOT NULL,

    CONSTRAINT chk_content_type
        CHECK (
            content_type IN (
                'VIDEO',
                'QUIZ',
                'ARTICLE',
                'LAB',
                'PROJECT'
            )
        ),

    CONSTRAINT chk_content_difficulty
        CHECK (
            difficulty IN (
                'BEGINNER',
                'INTERMEDIATE',
                'ADVANCED'
            )
        )
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;


-- =====================================================
-- 6. CONTENT SKILL
-- =====================================================

CREATE TABLE content_skill (
    content_id VARCHAR(20) NOT NULL,
    skill_id VARCHAR(20) NOT NULL,

    PRIMARY KEY (
        content_id,
        skill_id
    ),

    CONSTRAINT fk_content_skill_content
        FOREIGN KEY (content_id)
        REFERENCES content_items(content_id),

    CONSTRAINT fk_content_skill_skill
        FOREIGN KEY (skill_id)
        REFERENCES skills(skill_id)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;


-- =====================================================
-- 7. ATTEMPTS
-- =====================================================

CREATE TABLE attempts (
    attempt_id VARCHAR(50) PRIMARY KEY,
    learner_id VARCHAR(20) NOT NULL,
    content_id VARCHAR(20) NOT NULL,
    attempt_timestamp DATETIME NOT NULL,

    CONSTRAINT fk_attempt_learner
        FOREIGN KEY (learner_id)
        REFERENCES learners(learner_id),

    CONSTRAINT fk_attempt_content
        FOREIGN KEY (content_id)
        REFERENCES content_items(content_id),

    INDEX idx_attempt_learner (
        learner_id
    ),

    INDEX idx_attempt_content (
        content_id
    ),

    INDEX idx_attempt_timestamp (
        attempt_timestamp
    )
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;


-- =====================================================
-- 8. ASSESSMENT RESULTS
-- =====================================================

CREATE TABLE assessment_results (
    attempt_id VARCHAR(50) PRIMARY KEY,
    learner_id VARCHAR(20) NOT NULL,
    content_id VARCHAR(20) NOT NULL,
    score INT NOT NULL,
    pass_flag BOOLEAN NOT NULL,
    attempt_timestamp DATETIME NOT NULL,

    CONSTRAINT fk_assessment_attempt
        FOREIGN KEY (attempt_id)
        REFERENCES attempts(attempt_id),

    CONSTRAINT fk_assessment_learner
        FOREIGN KEY (learner_id)
        REFERENCES learners(learner_id),

    CONSTRAINT fk_assessment_content
        FOREIGN KEY (content_id)
        REFERENCES content_items(content_id),

    CONSTRAINT chk_assessment_score
        CHECK (
            score BETWEEN 0 AND 100
        ),

    INDEX idx_assessment_learner (
        learner_id
    ),

    INDEX idx_assessment_content (
        content_id
    )
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;


-- =====================================================
-- 9. MASTERY
-- =====================================================

CREATE TABLE mastery (
    learner_id VARCHAR(20) NOT NULL,
    skill_id VARCHAR(20) NOT NULL,
    mastery_score DECIMAL(6,4) NOT NULL,
    mastery_as_of_timestamp DATETIME NOT NULL,

    PRIMARY KEY (
        learner_id,
        skill_id,
        mastery_as_of_timestamp
    ),

    CONSTRAINT fk_mastery_learner
        FOREIGN KEY (learner_id)
        REFERENCES learners(learner_id),

    CONSTRAINT fk_mastery_skill
        FOREIGN KEY (skill_id)
        REFERENCES skills(skill_id),

    CONSTRAINT chk_mastery_score
        CHECK (
            mastery_score BETWEEN 0.0000 AND 1.0000
        ),

    INDEX idx_mastery_learner_skill (
        learner_id,
        skill_id
    )
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;


-- =====================================================
-- 10. RECOMMENDATIONS
-- =====================================================

CREATE TABLE recommendations (
    recommendation_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    learner_id VARCHAR(20) NOT NULL,
    previous_skill_id VARCHAR(20) NULL,
    recommended_skill_id VARCHAR(20) NOT NULL,
    recommended_content_id VARCHAR(20) NULL,
    reason_code VARCHAR(50) NOT NULL,
    target_difficulty VARCHAR(30) NULL,
    recommended_difficulty VARCHAR(30) NULL,
    difficulty_rank INT NULL,
    difficulty_match BOOLEAN NULL,

    CONSTRAINT fk_recommendation_learner
        FOREIGN KEY (learner_id)
        REFERENCES learners(learner_id),

    CONSTRAINT fk_recommendation_previous_skill
        FOREIGN KEY (previous_skill_id)
        REFERENCES skills(skill_id),

    CONSTRAINT fk_recommendation_skill
        FOREIGN KEY (recommended_skill_id)
        REFERENCES skills(skill_id),

    CONSTRAINT fk_recommendation_content
        FOREIGN KEY (recommended_content_id)
        REFERENCES content_items(content_id),

    CONSTRAINT chk_target_difficulty
        CHECK (
            target_difficulty IS NULL
            OR target_difficulty IN (
                'BEGINNER',
                'INTERMEDIATE',
                'ADVANCED'
            )
        ),

    CONSTRAINT chk_recommended_difficulty
        CHECK (
            recommended_difficulty IS NULL
            OR recommended_difficulty IN (
                'BEGINNER',
                'INTERMEDIATE',
                'ADVANCED'
            )
        ),

    CONSTRAINT chk_difficulty_rank
        CHECK (
            difficulty_rank IS NULL
            OR difficulty_rank BETWEEN 1 AND 3
        ),

    INDEX idx_recommendation_learner (
        learner_id
    ),

    INDEX idx_recommendation_skill (
        recommended_skill_id
    )
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;


-- =====================================================
-- 11. LEARNING PATHS
-- =====================================================

CREATE TABLE learning_paths (
    path_id VARCHAR(30) PRIMARY KEY,
    learner_id VARCHAR(20) NOT NULL,
    current_skill_id VARCHAR(20) NOT NULL,
    previous_skill_id VARCHAR(20) NULL,

    CONSTRAINT fk_learning_path_learner
        FOREIGN KEY (learner_id)
        REFERENCES learners(learner_id),

    CONSTRAINT fk_learning_path_current_skill
        FOREIGN KEY (current_skill_id)
        REFERENCES skills(skill_id),

    CONSTRAINT fk_learning_path_previous_skill
        FOREIGN KEY (previous_skill_id)
        REFERENCES skills(skill_id),

    INDEX idx_learning_path_learner (
        learner_id
    )
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;