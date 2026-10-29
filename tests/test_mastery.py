from src.events.mastery_generator import generate_mastery
from datetime import datetime

def test_mastery_calculation():
    assessment_results = [
        {"attempt_id": "ATT-001", "score": 55, "pass_flag": False},
        {"attempt_id": "ATT-002", "score": 68, "pass_flag": True},
        {"attempt_id": "ATT-003", "score": 74, "pass_flag": True},
        {"attempt_id": "ATT-004", "score": 82, "pass_flag": True},
        {"attempt_id": "ATT-005", "score": 91, "pass_flag": True},
    ]

    mastery_records = generate_mastery(assessment_results)

    assert len(mastery_records) == 1

    mastery = mastery_records[0]

    assert mastery["learner_id"] == "LRN-000001"
    assert mastery["skill_id"] == "SKL-000001"
    assert mastery["mastery_score"] == 0.74
def test_mastery_with_no_assessments():
    assessment_results = []

    mastery_records = generate_mastery(assessment_results)

    assert mastery_records == []
def test_mastery_ignores_future_assessments():
    assessment_results = [
        {
            "attempt_id": "ATT-001",
            "score": 55,
            "pass_flag": False,
            "attempt_timestamp": datetime(2026, 1, 15, 10, 0)
        },
        {
            "attempt_id": "ATT-002",
            "score": 68,
            "pass_flag": True,
            "attempt_timestamp": datetime(2026, 1, 16, 10, 0)
        },
        {
            "attempt_id": "ATT-003",
            "score": 74,
            "pass_flag": True,
            "attempt_timestamp": datetime(2026, 1, 17, 10, 0)
        },
        {
            "attempt_id": "ATT-004",
            "score": 82,
            "pass_flag": True,
            "attempt_timestamp": datetime(2026, 1, 18, 10, 0)
        },
        {
            "attempt_id": "ATT-005",
            "score": 91,
            "pass_flag": True,
            "attempt_timestamp": datetime(2026, 1, 19, 10, 0)
        }
    ]

    as_of_timestamp = datetime(2026, 1, 17, 23, 59, 59)

    mastery_records = generate_mastery(
        assessment_results,
        as_of_timestamp=as_of_timestamp
    )

    assert len(mastery_records) == 1

    assert mastery_records[0]["mastery_score"] == 0.6567
    assert (mastery_records[0]["mastery_as_of_timestamp"]== as_of_timestamp)
def test_mastery_returns_empty_when_all_assessments_are_future():
    assessment_results = [
        {
            "attempt_id": "ATT-001",
            "score": 80,
            "pass_flag": True,
            "attempt_timestamp": datetime(2026, 1, 15, 10, 0)
        },
        {
            "attempt_id": "ATT-002",
            "score": 90,
            "pass_flag": True,
            "attempt_timestamp": datetime(2026, 1, 16, 10, 0)
        }
    ]

    as_of_timestamp = datetime(2026, 1, 14, 23, 59, 59)

    mastery_records = generate_mastery(
        assessment_results,
        as_of_timestamp=as_of_timestamp
    )

    assert mastery_records == []
def test_mastery_is_calculated_per_learner_and_skill():
    assessment_results = [
        {
            "attempt_id": "ATT-001",
            "learner_id": "LRN-000001",
            "content_id": "CNT-000001",
            "score": 55,
            "pass_flag": False,
            "attempt_timestamp": datetime(
                2026, 1, 15, 10, 0
            ),
        },
        {
            "attempt_id": "ATT-002",
            "learner_id": "LRN-000002",
            "content_id": "CNT-000002",
            "score": 68,
            "pass_flag": True,
            "attempt_timestamp": datetime(
                2026, 1, 16, 10, 0
            ),
        },
        {
            "attempt_id": "ATT-003",
            "learner_id": "LRN-000003",
            "content_id": "CNT-000003",
            "score": 74,
            "pass_flag": True,
            "attempt_timestamp": datetime(
                2026, 1, 17, 10, 0
            ),
        },
    ]

    content_skill_mapping = [
        {
            "content_id": "CNT-000001",
            "skill_id": "SKL-000001",
        },
        {
            "content_id": "CNT-000002",
            "skill_id": "SKL-000002",
        },
        {
            "content_id": "CNT-000003",
            "skill_id": "SKL-000003",
        },
    ]

    as_of_timestamp = datetime(
        2026, 1, 17, 23, 59, 59
    )

    mastery_records = generate_mastery(
        assessment_results,
        as_of_timestamp=as_of_timestamp,
        content_skill_mapping=content_skill_mapping,
    )

    mastery_lookup = {
        (
            record["learner_id"],
            record["skill_id"],
        ): record["mastery_score"]
        for record in mastery_records
    }

    assert len(mastery_records) == 3

    assert mastery_lookup[
        ("LRN-000001", "SKL-000001")
    ] == 0.55

    assert mastery_lookup[
        ("LRN-000002", "SKL-000002")
    ] == 0.68

    assert mastery_lookup[
        ("LRN-000003", "SKL-000003")
    ] == 0.74