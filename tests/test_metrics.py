from src.metrics.metrics_calculator import (
    calculate_metrics,
)


def test_metrics_calculation():
    learners = [
        {"learner_id": "LRN-000001"},
        {"learner_id": "LRN-000002"},
        {"learner_id": "LRN-000003"},
        {"learner_id": "LRN-000004"},
    ]

    assessment_results = [
        {
            "attempt_id": "ATT-001",
            "pass_flag": True,
        },
        {
            "attempt_id": "ATT-002",
            "pass_flag": True,
        },
        {
            "attempt_id": "ATT-003",
            "pass_flag": False,
        },
        {
            "attempt_id": "ATT-004",
            "pass_flag": False,
        },
    ]

    recommendations = [
        {
            "learner_id": "LRN-000001",
            "reason_code": "LOW_MASTERY_REVIEW",
            "difficulty_match": True,
        },
        {
            "learner_id": "LRN-000002",
            "reason_code": "LOW_MASTERY_REVIEW",
            "difficulty_match": False,
        },
        {
            "learner_id": "LRN-000003",
            "reason_code": "COLD_START_DEFAULT",
            "difficulty_match": True,
        },
    ]

    validation_issues = [
        {
            "issue_type": "PREREQUISITE_VIOLATION",
        }
    ]

    metrics = calculate_metrics(
        learners=learners,
        assessment_results=assessment_results,
        recommendations=recommendations,
        validation_issues=validation_issues,
    )

    assert metrics["total_learners"] == 4
    assert metrics["total_assessments"] == 4
    assert metrics["total_recommendations"] == 3

    assert (
        metrics["recommendation_coverage"]
        == 0.75
    )

    assert metrics["pass_rate"] == 0.5

    assert (
        metrics["difficulty_match_rate"]
        == 0.6667
    )

    assert (
        metrics["cold_start_rate"]
        == 0.3333
    )

    assert (
        metrics["prerequisite_violation_rate"]
        == 0.3333
    )


def test_metrics_handle_empty_data():
    metrics = calculate_metrics(
        learners=[],
        assessment_results=[],
        recommendations=[],
        validation_issues=[],
    )

    assert metrics["total_learners"] == 0
    assert metrics["total_assessments"] == 0
    assert metrics["total_recommendations"] == 0

    assert metrics["recommendation_coverage"] == 0.0
    assert metrics["pass_rate"] == 0.0
    assert metrics["difficulty_match_rate"] == 0.0
    assert metrics["cold_start_rate"] == 0.0

    assert (
        metrics["prerequisite_violation_rate"]
        == 0.0
    )