def inject_prerequisite_violation(recommendations):
    """
    Inject one controlled prerequisite violation.

    Returns:
        modified recommendations
        ground-truth anomaly record
    """

    modified_recommendations = [
        recommendation.copy()
        for recommendation in recommendations
    ]

    if not modified_recommendations:
        return modified_recommendations, None

    target = modified_recommendations[0]

    original_skill_id = target[
        "recommended_skill_id"
    ]

    # Intentionally jump ahead in the learning graph.
    target["recommended_skill_id"] = "SKL-000005"

    ground_truth = {
        "anomaly_id": "ANM-000001",
        "entity_type": "RECOMMENDATION",
        "entity_id": target["learner_id"],
        "issue_type": "PREREQUISITE_VIOLATION",
        "description": (
            "Recommendation intentionally bypasses "
            "required skill prerequisites."
        ),
        "original_skill_id": original_skill_id,
        "anomalous_skill_id": "SKL-000005",
    }

    return modified_recommendations, ground_truth