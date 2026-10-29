from src.events.learning_path_generator import (
    generate_learning_paths
)


def test_learning_path_matches_recommendation():
    recommendations = [
        {
            "learner_id": "LRN-000001",
            "recommended_skill_id": "SKL-000001",
            "reason_code": "LOW_MASTERY_REVIEW"
        }
    ]

    learning_paths = generate_learning_paths(
        recommendations
    )

    assert len(learning_paths) == 1

    path = learning_paths[0]

    assert path["learner_id"] == "LRN-000001"
    assert path["current_skill_id"] == "SKL-000001"
    assert path["previous_skill_id"] == "SKL-000001"
def test_learning_path_advances_with_recommendation():
    recommendations = [
    {
        "learner_id": "LRN-000001",
        "previous_skill_id": "SKL-000001",
        "recommended_skill_id": "SKL-000002",
        "reason_code": "PREREQ_MET"
    }
]

    learning_paths = generate_learning_paths(
        recommendations
    )

    assert len(learning_paths) == 1

    path = learning_paths[0]

    assert path["learner_id"] == "LRN-000001"
    assert path["previous_skill_id"] == "SKL-000001"
    assert path["current_skill_id"] == "SKL-000002"
    assert path["path_id"] == "PATH-2026-000001"




