def validate_attempt_timestamp_order(attempts):
    """
    Validate chronological ordering of attempts.

    Assumes records are provided in their intended
    event sequence.

    Returns:
        list of validation issue dictionaries
    """

    issues = []

    if len(attempts) < 2:
        return issues

    previous_attempt = attempts[0]

    for current_attempt in attempts[1:]:
        previous_timestamp = previous_attempt[
            "attempt_timestamp"
        ]

        current_timestamp = current_attempt[
            "attempt_timestamp"
        ]

        if current_timestamp < previous_timestamp:
            issues.append(
                {
                    "entity_type": "ATTEMPT",
                    "entity_id": current_attempt[
                        "attempt_id"
                    ],
                    "issue_type": (
                        "INVALID_ATTEMPT_TIMESTAMP_ORDER"
                    ),
                    "previous_timestamp": (
                        previous_timestamp
                    ),
                    "current_timestamp": (
                        current_timestamp
                    ),
                }
            )

        previous_attempt = current_attempt

    return issues