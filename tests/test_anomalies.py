from datetime import datetime

from src.anomalies.prerequisite_violation import (
    inject_prerequisite_violation,
)
from src.anomalies.invalid_attempt_timestamp import (
    inject_invalid_attempt_timestamp,
)
from src.anomalies.invalid_content_skill import (
    inject_invalid_content_skill,
)
from src.anomalies.future_mastery_leakage import (
    inject_future_mastery_leakage,
)
from src.anomalies.learning_path_loop import (
    inject_learning_path_loop,
)
from src.anomalies.learning_path_loop import (
    inject_learning_path_loop,
)

def test_prerequisite_violation_injection():
    clean_recommendations = [
        {
            "learner_id": "LRN-000001",
            "recommended_skill_id": "SKL-000001",
            "recommended_content_id": "CNT-000001",
            "reason_code": "LOW_MASTERY_REVIEW",
        }
    ]

    anomalous_recommendations, ground_truth = (
        inject_prerequisite_violation(
            clean_recommendations
        )
    )

    # Clean baseline remains unchanged.
    assert (
        clean_recommendations[0][
            "recommended_skill_id"
        ]
        == "SKL-000001"
    )

    # Injected copy intentionally skips prerequisites.
    assert (
        anomalous_recommendations[0][
            "recommended_skill_id"
        ]
        == "SKL-000005"
    )

    assert ground_truth is not None

    assert (
        ground_truth["issue_type"]
        == "PREREQUISITE_VIOLATION"
    )

    assert (
        ground_truth["entity_type"]
        == "RECOMMENDATION"
    )

    assert (
        ground_truth["original_skill_id"]
        == "SKL-000001"
    )

    assert (
        ground_truth["anomalous_skill_id"]
        == "SKL-000005"
    )


def test_invalid_attempt_timestamp_injection():
    clean_attempts = [
        {
            "attempt_id": "ATT-001",
            "learner_id": "LRN-000001",
            "content_id": "CNT-000001",
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
            "learner_id": "LRN-000001",
            "content_id": "CNT-000002",
            "attempt_timestamp": datetime(
                2026,
                1,
                16,
                10,
                0,
            ),
        },
    ]

    anomalous_attempts, ground_truth = (
        inject_invalid_attempt_timestamp(
            clean_attempts
        )
    )

    # Clean baseline remains unchanged.
    assert (
        clean_attempts[1]["attempt_timestamp"]
        == datetime(2026, 1, 16, 10, 0)
    )

    # Injected attempt occurs before the first attempt.
    assert (
        anomalous_attempts[1]["attempt_timestamp"]
        < anomalous_attempts[0]["attempt_timestamp"]
    )

    assert ground_truth is not None

    assert (
        ground_truth["issue_type"]
        == "INVALID_ATTEMPT_TIMESTAMP_ORDER"
    )

    assert (
        ground_truth["entity_type"]
        == "ATTEMPT"
    )

    assert ground_truth["entity_id"] == "ATT-002"


def test_invalid_content_skill_injection():
    clean_mapping = [
        {
            "content_id": "CNT-000001",
            "skill_id": "SKL-000001",
        },
        {
            "content_id": "CNT-000002",
            "skill_id": "SKL-000002",
        },
    ]

    anomalous_mapping, ground_truth = (
        inject_invalid_content_skill(
            clean_mapping
        )
    )

    # Clean baseline remains unchanged.
    assert (
        clean_mapping[0]["skill_id"]
        == "SKL-000001"
    )

    # Injected copy references a nonexistent skill.
    assert (
        anomalous_mapping[0]["skill_id"]
        == "SKL-999999"
    )

    assert ground_truth is not None

    assert (
        ground_truth["issue_type"]
        == "INVALID_CONTENT_SKILL_REFERENCE"
    )

    assert (
        ground_truth["entity_type"]
        == "CONTENT_SKILL"
    )

    assert (
        ground_truth["original_skill_id"]
        == "SKL-000001"
    )

    assert (
        ground_truth["anomalous_skill_id"]
        == "SKL-999999"
    )


def test_future_mastery_leakage_injection():
    as_of_timestamp = datetime(
        2026,
        1,
        17,
        23,
        59,
        59,
    )

    clean_mastery = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000001",
            "mastery_score": 0.55,
            "mastery_as_of_timestamp": (
                as_of_timestamp
            ),
        }
    ]

    anomalous_mastery, ground_truth = (
        inject_future_mastery_leakage(
            clean_mastery
        )
    )

    # Clean baseline remains unchanged.
    assert (
        "future_source_timestamp"
        not in clean_mastery[0]
    )

    # Injected source evidence occurs after cutoff.
    assert (
        anomalous_mastery[0][
            "future_source_timestamp"
        ]
        > anomalous_mastery[0][
            "mastery_as_of_timestamp"
        ]
    )

    assert ground_truth is not None

    assert (
        ground_truth["issue_type"]
        == "FUTURE_MASTERY_LEAKAGE"
    )

    assert (
        ground_truth["entity_type"]
        == "MASTERY"
    )

    assert (
        ground_truth["future_source_timestamp"]
        > ground_truth["mastery_as_of_timestamp"]
    )

    assert (
        ground_truth["entity_id"]
        == "LRN-000001:SKL-000001"
    )
def test_learning_path_loop_injection():
    clean_paths = [
        {
            "path_id": "PATH-2026-000001",
            "learner_id": "LRN-000001",
            "previous_skill_id": "SKL-000001",
            "current_skill_id": "SKL-000002",
        }
    ]

    anomalous_paths, ground_truth = (
        inject_learning_path_loop(
            clean_paths
        )
    )

    # Clean baseline must stay unchanged.
    assert (
        clean_paths[0]["previous_skill_id"]
        == "SKL-000001"
    )

    assert (
        clean_paths[0]["current_skill_id"]
        == "SKL-000002"
    )

    # Injected path must contain no progression.
    assert (
        anomalous_paths[0]["previous_skill_id"]
        == anomalous_paths[0]["current_skill_id"]
    )

    assert ground_truth is not None

    assert (
        ground_truth["issue_type"]
        == "LEARNING_PATH_LOOP"
    )

    assert (
        ground_truth["entity_type"]
        == "LEARNING_PATH"
    )

    assert (
        ground_truth["entity_id"]
        == "PATH-2026-000001"
    )
