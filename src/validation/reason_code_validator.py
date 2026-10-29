VALID_REASON_CODES = {
    "PREREQ_MET",
    "LOW_MASTERY_REVIEW",
    "RETRY_FAILED_CONTENT",
    "COLD_START_DEFAULT",
}


def validate_reason_codes(
    recommendations,
):
    """
    Validate recommendation reason codes.
    """

    issues = []

    for recommendation in recommendations:
        reason_code = recommendation.get(
            "reason_code"
        )

        if reason_code not in VALID_REASON_CODES:
            issues.append(
                {
                    "entity_type": "RECOMMENDATION",
                    "entity_id": recommendation.get(
                        "learner_id"
                    ),
                    "issue_type": (
                        "INVALID_REASON_CODE"
                    ),
                    "reason_code": reason_code,
                }
            )

    return issues