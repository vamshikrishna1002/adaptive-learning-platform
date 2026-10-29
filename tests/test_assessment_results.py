from datetime import datetime, timedelta

from src.events.attempt_generator import generate_attempts
from src.events.assessment_result_generator import (
    generate_assessment_results,
)


def test_assessment_results_derive_pass_flag():
    base_time = datetime(2026, 1, 15, 10, 0, 0)

    attempts = [
        {
            "attempt_id": f"ATT-LRN-000001-{number:06d}",
            "learner_id": "LRN-000001",
            "content_id": f"CNT-{number:06d}",
            "attempt_timestamp": (
                base_time + timedelta(days=number - 1)
            ),
        }
        for number in range(1, 6)
    ]

    results = generate_assessment_results(attempts)

    assert len(results) == 5

    for attempt, result in zip(attempts, results):
        expected_pass_flag = result["score"] >= 60

        assert result["pass_flag"] == expected_pass_flag

        # Verify source lineage is preserved.
        assert result["attempt_id"] == attempt["attempt_id"]
        assert result["learner_id"] == attempt["learner_id"]
        assert result["content_id"] == attempt["content_id"]

        assert (
            result["attempt_timestamp"]
            == attempt["attempt_timestamp"]
        )


def test_assessment_result_count_matches_attempt_count():
    attempts = generate_attempts(
        count=500,
        content_count=5,
        learner_count=90,
    )

    results = generate_assessment_results(attempts)

    assert len(results) == len(attempts)
    assert len(results) == 500


def test_assessment_count_matches_attempt_count():
    attempts = generate_attempts(
        count=500,
        content_count=5,
        learner_count=90,
    )

    results = generate_assessment_results(attempts)

    assert len(attempts) == 500
    assert len(results) == 500
    assert len(results) == len(attempts)