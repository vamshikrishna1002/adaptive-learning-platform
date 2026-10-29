def validate_mastery_temporal_integrity(
    mastery_records,
):
    """
    Detect mastery records that reference
    source evidence occurring after the
    as-of timestamp.
    """

    issues = []

    for record in mastery_records:
        as_of_timestamp = record.get(
            "mastery_as_of_timestamp"
        )

        future_timestamp = record.get(
            "future_source_timestamp"
        )

        if (
            as_of_timestamp is not None
            and future_timestamp is not None
            and future_timestamp > as_of_timestamp
        ):
            issues.append(
                {
                    "entity_type": "MASTERY",
                    "entity_id": (
                        f"{record['learner_id']}:"
                        f"{record['skill_id']}"
                    ),
                    "issue_type": (
                        "FUTURE_MASTERY_LEAKAGE"
                    ),
                }
            )

    return issues