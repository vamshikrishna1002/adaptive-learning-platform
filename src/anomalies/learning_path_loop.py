def inject_learning_path_loop(learning_paths):
    """
    Inject one controlled learning-path loop.

    The clean baseline remains unchanged.
    """

    modified_paths = [
        path.copy()
        for path in learning_paths
    ]

    if not modified_paths:
        return modified_paths, None

    target = modified_paths[0]

    original_current_skill = target[
        "current_skill_id"
    ]

    original_previous_skill = target[
        "previous_skill_id"
    ]

    # Intentionally create a no-progress loop.
    target["previous_skill_id"] = (
        original_current_skill
    )

    target["current_skill_id"] = (
        original_current_skill
    )

    ground_truth = {
        "anomaly_id": "ANM-000005",
        "entity_type": "LEARNING_PATH",
        "entity_id": target["path_id"],
        "issue_type": "LEARNING_PATH_LOOP",
        "description": (
            "Learning path intentionally remains "
            "on the same skill without progression."
        ),
        "original_previous_skill_id": (
            original_previous_skill
        ),
        "original_current_skill_id": (
            original_current_skill
        ),
        "anomalous_previous_skill_id": (
            target["previous_skill_id"]
        ),
        "anomalous_current_skill_id": (
            target["current_skill_id"]
        ),
    }

    return modified_paths, ground_truth