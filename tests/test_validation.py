from datetime import datetime

from src.validation.pk_validator import (
    validate_primary_key_uniqueness,
)
from src.validation.fk_validator import (
    validate_foreign_key,
)
from src.validation.timestamp_validator import (
    validate_attempt_timestamp_order,
)
from src.validation.mastery_validator import (
    validate_mastery_temporal_integrity,
)
from src.validation.prerequisite_validator import (
    validate_prerequisite_compliance,
)
from src.validation.learning_path_validator import (
    validate_learning_path_loops,
)
from src.validation.validation_runner import (
    run_validation,
)

from src.generators.learner_generator import (
    generate_learners,
)
from src.generators.course_generator import (
    generate_courses,
)
from src.generators.skill_generator import (
    generate_skills,
)
from src.generators.skill_prerequisite_generator import (
    generate_skill_prerequisites,
)
from src.generators.content_generator import (
    generate_content_items,
)
from src.generators.content_skill_generator import (
    generate_content_skill_mapping,
)

from src.events.attempt_generator import (
    generate_attempts,
)
from src.events.assessment_result_generator import (
    generate_assessment_results,
)


# -----------------------------------------------------
# PRIMARY KEY VALIDATION
# -----------------------------------------------------


def test_primary_key_validation_passes_for_unique_ids():
    records = [
        {"learner_id": "LRN-000001"},
        {"learner_id": "LRN-000002"},
        {"learner_id": "LRN-000003"},
    ]

    issues = validate_primary_key_uniqueness(
        records=records,
        key_field="learner_id",
        entity_type="LEARNER",
    )

    assert issues == []


def test_primary_key_validation_detects_duplicate():
    records = [
        {"learner_id": "LRN-000001"},
        {"learner_id": "LRN-000002"},
        {"learner_id": "LRN-000001"},
    ]

    issues = validate_primary_key_uniqueness(
        records=records,
        key_field="learner_id",
        entity_type="LEARNER",
    )

    assert len(issues) == 1

    issue = issues[0]

    assert issue["entity_type"] == "LEARNER"

    assert (
        issue["issue_type"]
        == "DUPLICATE_PRIMARY_KEY"
    )

    assert issue["field"] == "learner_id"

    assert (
        issue["value"]
        == "LRN-000001"
    )


# -----------------------------------------------------
# FOREIGN KEY VALIDATION
# -----------------------------------------------------


def test_foreign_key_validation_passes_for_valid_reference():
    learners = [
        {"learner_id": "LRN-000001"},
        {"learner_id": "LRN-000002"},
    ]

    attempts = [
        {
            "attempt_id": "ATT-001",
            "learner_id": "LRN-000001",
        },
        {
            "attempt_id": "ATT-002",
            "learner_id": "LRN-000002",
        },
    ]

    issues = validate_foreign_key(
        child_records=attempts,
        child_field="learner_id",
        parent_records=learners,
        parent_field="learner_id",
        entity_type="ATTEMPT",
    )

    assert issues == []


def test_foreign_key_validation_detects_invalid_reference():
    learners = [
        {"learner_id": "LRN-000001"},
        {"learner_id": "LRN-000002"},
    ]

    attempts = [
        {
            "attempt_id": "ATT-001",
            "learner_id": "LRN-999999",
        }
    ]

    issues = validate_foreign_key(
        child_records=attempts,
        child_field="learner_id",
        parent_records=learners,
        parent_field="learner_id",
        entity_type="ATTEMPT",
    )

    assert len(issues) == 1

    issue = issues[0]

    assert issue["entity_type"] == "ATTEMPT"

    assert (
        issue["issue_type"]
        == "INVALID_FOREIGN_KEY"
    )

    assert issue["field"] == "learner_id"

    assert (
        issue["value"]
        == "LRN-999999"
    )

    assert (
        issue["parent_field"]
        == "learner_id"
    )


# -----------------------------------------------------
# CLEAN BASELINE VALIDATION
# -----------------------------------------------------


def test_validation_runner_on_clean_baseline():
    learners = generate_learners(10)

    courses = generate_courses(5)

    skills = generate_skills(5)

    skill_prerequisites = (
        generate_skill_prerequisites()
    )

    content_items = (
        generate_content_items(5)
    )

    content_skill_mapping = (
        generate_content_skill_mapping(
            content_count=5,
            skill_count=5,
        )
    )

    attempts = generate_attempts(
        count=5,
        content_count=5,
        learner_count=5,
    )

    assessment_results = (
        generate_assessment_results(
            attempts
        )
    )

    issues = run_validation(
        learners=learners,
        courses=courses,
        skills=skills,
        content_items=content_items,
        content_skill_mapping=(
            content_skill_mapping
        ),
        attempts=attempts,
        assessment_results=(
            assessment_results
        ),
        mastery_records=[],
        recommendations=[],
        learning_paths=[],
        skill_prerequisites=(
            skill_prerequisites
        ),
    )

    assert issues == []


# -----------------------------------------------------
# GROUND TRUTH ANOMALY DETECTION
# -----------------------------------------------------


def test_validators_detect_all_ground_truth_anomaly_types():
    detected_issue_types = set()

    # -------------------------------------------------
    # 1. PREREQUISITE_VIOLATION
    # -------------------------------------------------

    recommendations = [
        {
            "learner_id": "LRN-000001",
            "previous_skill_id": "SKL-000001",
            "recommended_skill_id": "SKL-000005",
        }
    ]

    prerequisites = [
        {
            "parent_skill_id": "SKL-000001",
            "child_skill_id": "SKL-000002",
        }
    ]

    issues = validate_prerequisite_compliance(
        recommendations,
        prerequisites,
    )

    detected_issue_types.update(
        issue["issue_type"]
        for issue in issues
    )

    # -------------------------------------------------
    # 2. INVALID_ATTEMPT_TIMESTAMP_ORDER
    # -------------------------------------------------

    attempts = [
        {
            "attempt_id": "ATT-001",
            "attempt_timestamp": datetime(
                2026,
                1,
                15,
                10,
                0,
            ),
        },
        {
            "attempt_id": "ATT-002",
            "attempt_timestamp": datetime(
                2026,
                1,
                14,
                10,
                0,
            ),
        },
    ]

    issues = (
        validate_attempt_timestamp_order(
            attempts
        )
    )

    detected_issue_types.update(
        issue["issue_type"]
        for issue in issues
    )

    # -------------------------------------------------
    # 3. INVALID_CONTENT_SKILL_REFERENCE
    # -------------------------------------------------

    skills = [
        {
            "skill_id": "SKL-000001",
        }
    ]

    invalid_mapping = [
        {
            "content_id": "CNT-000001",
            "skill_id": "SKL-999999",
        }
    ]

    issues = validate_foreign_key(
        child_records=invalid_mapping,
        child_field="skill_id",
        parent_records=skills,
        parent_field="skill_id",
        entity_type="CONTENT_SKILL",
    )

    if issues:
        detected_issue_types.add(
            "INVALID_CONTENT_SKILL_REFERENCE"
        )

    # -------------------------------------------------
    # 4. FUTURE_MASTERY_LEAKAGE
    # -------------------------------------------------

    mastery_records = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000001",
            "mastery_as_of_timestamp": datetime(
                2026,
                1,
                17,
                23,
                59,
                59,
            ),
            "future_source_timestamp": datetime(
                2026,
                1,
                18,
                23,
                59,
                59,
            ),
        }
    ]

    issues = (
        validate_mastery_temporal_integrity(
            mastery_records
        )
    )

    detected_issue_types.update(
        issue["issue_type"]
        for issue in issues
    )

    # -------------------------------------------------
    # 5. LEARNING_PATH_LOOP
    # -------------------------------------------------

    learning_paths = [
        {
            "path_id": "PATH-2026-000001",
            "previous_skill_id": "SKL-000001",
            "current_skill_id": "SKL-000001",
        }
    ]

    issues = validate_learning_path_loops(
        learning_paths
    )

    detected_issue_types.update(
        issue["issue_type"]
        for issue in issues
    )

    expected_issue_types = {
        "PREREQUISITE_VIOLATION",
        "INVALID_ATTEMPT_TIMESTAMP_ORDER",
        "INVALID_CONTENT_SKILL_REFERENCE",
        "FUTURE_MASTERY_LEAKAGE",
        "LEARNING_PATH_LOOP",
    }

    assert (
        detected_issue_types
        == expected_issue_types
    )