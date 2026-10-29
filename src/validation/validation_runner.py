from src.validation.pk_validator import (
    validate_primary_key_uniqueness,
)
from src.validation.fk_validator import (
    validate_foreign_key,
)
from src.validation.duplicate_validator import (
    validate_duplicates,
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
from src.validation.reason_code_validator import (
    validate_reason_codes,
)
from src.validation.enum_validator import (
    validate_enum_values,
)


def run_validation(
    learners,
    courses,
    skills,
    content_items,
    content_skill_mapping,
    attempts,
    assessment_results,
    mastery_records,
    recommendations,
    learning_paths,
    skill_prerequisites,
):
    """
    Run the complete validation suite.

    Returns:
        list of validation issue dictionaries
    """

    issues = []

    # ---------------------------------------------
    # Primary keys
    # ---------------------------------------------

    pk_checks = [
        (learners, "learner_id", "LEARNER"),
        (courses, "course_id", "COURSE"),
        (skills, "skill_id", "SKILL"),
        (
            content_items,
            "content_id",
            "CONTENT_ITEM",
        ),
        (attempts, "attempt_id", "ATTEMPT"),
        (
            learning_paths,
            "path_id",
            "LEARNING_PATH",
        ),
    ]

    for records, key_field, entity_type in pk_checks:
        issues.extend(
            validate_primary_key_uniqueness(
                records,
                key_field,
                entity_type,
            )
        )

    # ---------------------------------------------
    # Foreign keys
    # ---------------------------------------------

    fk_checks = [
        (
            attempts,
            "learner_id",
            learners,
            "learner_id",
            "ATTEMPT",
        ),
        (
            attempts,
            "content_id",
            content_items,
            "content_id",
            "ATTEMPT",
        ),
        (
            assessment_results,
            "attempt_id",
            attempts,
            "attempt_id",
            "ASSESSMENT_RESULT",
        ),
        (
            content_skill_mapping,
            "content_id",
            content_items,
            "content_id",
            "CONTENT_SKILL",
        ),
        (
            content_skill_mapping,
            "skill_id",
            skills,
            "skill_id",
            "CONTENT_SKILL",
        ),
        (
            mastery_records,
            "learner_id",
            learners,
            "learner_id",
            "MASTERY",
        ),
        (
            mastery_records,
            "skill_id",
            skills,
            "skill_id",
            "MASTERY",
        ),
    ]

    for (
        child_records,
        child_field,
        parent_records,
        parent_field,
        entity_type,
    ) in fk_checks:
        issues.extend(
            validate_foreign_key(
                child_records,
                child_field,
                parent_records,
                parent_field,
                entity_type,
            )
        )

    # ---------------------------------------------
    # Duplicate bridge records
    # ---------------------------------------------

    issues.extend(
    validate_learning_path_loops(
        learning_paths=learning_paths,
        recommendations=recommendations,
        skill_prerequisites=skill_prerequisites,
            )
        )

    # ---------------------------------------------
    # Attempt timestamp ordering
    # ---------------------------------------------

    issues.extend(
        validate_attempt_timestamp_order(
            attempts
        )
    )

    # ---------------------------------------------
    # Mastery temporal integrity
    # ---------------------------------------------

    issues.extend(
        validate_mastery_temporal_integrity(
            mastery_records
        )
    )

    # ---------------------------------------------
    # Recommendation prerequisites
    # ---------------------------------------------

    issues.extend(
        validate_prerequisite_compliance(
            recommendations,
            skill_prerequisites,
        )
    )

    # ---------------------------------------------
    # Learning path loops
    # ---------------------------------------------

    issues.extend(
        validate_learning_path_loops(
            learning_paths,
            recommendations,
        )
    )

    # ---------------------------------------------
    # Recommendation reason codes
    # ---------------------------------------------

    issues.extend(
        validate_reason_codes(
            recommendations
        )
    )

    # ---------------------------------------------
    # Enum validation
    # ---------------------------------------------

    issues.extend(
        validate_enum_values(
            learners,
            "learner_status",
            {
                "REGISTERED",
                "ACTIVE",
                "INACTIVE",
                "SUSPENDED",
            },
            "LEARNER",
        )
    )

    issues.extend(
        validate_enum_values(
            content_items,
            "content_type",
            {
                "VIDEO",
                "QUIZ",
                "ARTICLE",
                "LAB",
                "PROJECT",
            },
            "CONTENT_ITEM",
        )
    )

    issues.extend(
        validate_enum_values(
            content_items,
            "difficulty",
            {
                "BEGINNER",
                "INTERMEDIATE",
                "ADVANCED",
            },
            "CONTENT_ITEM",
        )
    )

    return issues