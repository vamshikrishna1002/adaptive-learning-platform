def validate_prerequisite_compliance(
    recommendations,
    skill_prerequisites,
):
    """
    Detect recommendations that jump over
    the prerequisite graph.
    """

    issues = []

    allowed_transitions = {
        (
            relationship["parent_skill_id"],
            relationship["child_skill_id"],
        )
        for relationship in skill_prerequisites
    }

    for recommendation in recommendations:
        previous_skill = recommendation.get(
            "previous_skill_id"
        )

        recommended_skill = recommendation.get(
            "recommended_skill_id"
        )

        # Staying on the same skill is valid review behavior.
        if previous_skill == recommended_skill:
            continue

        # Cold-start recommendation has no previous skill.
        if previous_skill is None:
            continue

        transition = (
            previous_skill,
            recommended_skill,
        )

        if transition not in allowed_transitions:
            issues.append(
                {
                    "entity_type": "RECOMMENDATION",
                    "entity_id": recommendation.get(
                        "learner_id"
                    ),
                    "issue_type": (
                        "PREREQUISITE_VIOLATION"
                    ),
                    "previous_skill_id": (
                        previous_skill
                    ),
                    "recommended_skill_id": (
                        recommended_skill
                    ),
                }
            )

    return issues