def validate_learning_path_loops(
    learning_paths,
    recommendations=None,
    skill_prerequisites=None,
):
    """
    Detect invalid learning-path loops.

    Same-skill paths are valid when:
    - the recommendation requests review or retry;
    - the learner is at a terminal skill with no child skill;
    - the path is a cold-start path.

    A same-skill path is invalid when advancement
    was expected and another skill exists.
    """

    issues = []

    recommendation_lookup = {}

    if recommendations is not None:
        recommendation_lookup = {
            recommendation["learner_id"]: recommendation
            for recommendation in recommendations
        }

    parent_skills = set()

    if skill_prerequisites is not None:
        parent_skills = {
            relationship["parent_skill_id"]
            for relationship in skill_prerequisites
        }

    valid_same_skill_reasons = {
        "LOW_MASTERY_REVIEW",
        "RETRY_FAILED_CONTENT",
        "COLD_START_DEFAULT",
    }

    for path in learning_paths:
        learner_id = path.get(
            "learner_id"
        )

        previous_skill = path.get(
            "previous_skill_id"
        )

        current_skill = path.get(
            "current_skill_id"
        )

        # Cold-start path.
        if previous_skill is None:
            continue

        # The learner progressed to another skill.
        if previous_skill != current_skill:
            continue

        recommendation = recommendation_lookup.get(
            learner_id
        )

        # Review and retry recommendations may
        # legitimately remain on the same skill.
        if recommendation is not None:
            reason_code = recommendation.get(
                "reason_code"
            )

            if reason_code in valid_same_skill_reasons:
                continue

        # A skill not appearing as a parent has no
        # child skill and is therefore terminal.
        if (
            skill_prerequisites is not None
            and current_skill not in parent_skills
        ):
           continue

        issues.append(
            {
                "entity_type": "LEARNING_PATH",
                "entity_id": path.get(
                    "path_id"
                ),
                "issue_type": "LEARNING_PATH_LOOP",
                "previous_skill_id": previous_skill,
                "current_skill_id": current_skill,
            }
        )

    return issues