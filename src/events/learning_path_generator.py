def generate_learning_paths(recommendations):
    learning_paths = []

    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):
        recommended_skill_id = recommendation[
            "recommended_skill_id"
        ]

        learning_paths.append(
            {
                "path_id": f"PATH-2026-{index:06d}",
                "learner_id": recommendation["learner_id"],
                "current_skill_id": recommended_skill_id,
                "previous_skill_id": recommendation.get("previous_skill_id",recommended_skill_id)
            }
        )

    return learning_paths
