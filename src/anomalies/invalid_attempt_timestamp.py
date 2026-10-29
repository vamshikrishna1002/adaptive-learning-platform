from datetime import timedelta


def inject_invalid_attempt_timestamp(attempts):
    """
    Inject one invalid attempt timestamp while
    preserving the original clean dataset.

    Returns:
        modified attempts
        ground-truth anomaly record
    """

    modified_attempts = [
        attempt.copy()
        for attempt in attempts
    ]

    if len(modified_attempts) < 2:
        return modified_attempts, None

    target = modified_attempts[1]

    original_timestamp = target[
        "attempt_timestamp"
    ]

    # Intentionally place attempt 2 before attempt 1.
    anomalous_timestamp = (
        modified_attempts[0]["attempt_timestamp"]
        - timedelta(days=1)
    )

    target["attempt_timestamp"] = (
        anomalous_timestamp
    )

    ground_truth = {
        "anomaly_id": "ANM-000002",
        "entity_type": "ATTEMPT",
        "entity_id": target["attempt_id"],
        "issue_type": (
            "INVALID_ATTEMPT_TIMESTAMP_ORDER"
        ),
        "description": (
            "Attempt timestamp intentionally occurs "
            "before the preceding attempt."
        ),
        "original_timestamp": (
            original_timestamp
        ),
        "anomalous_timestamp": (
            anomalous_timestamp
        ),
    }

    return modified_attempts, ground_truth