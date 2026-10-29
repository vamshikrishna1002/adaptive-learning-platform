from datetime import timedelta


def inject_future_mastery_leakage(mastery_records):
    """
    Inject one controlled future-data leakage anomaly.

    The original clean mastery records remain unchanged.
    """

    modified_mastery = [
        record.copy()
        for record in mastery_records
    ]

    if not modified_mastery:
        return modified_mastery, None

    target = modified_mastery[0]

    original_as_of_timestamp = target.get(
        "mastery_as_of_timestamp"
    )

    if original_as_of_timestamp is None:
        return modified_mastery, None

    # Represents source evidence occurring after
    # the mastery calculation cutoff.
    future_source_timestamp = (
        original_as_of_timestamp
        + timedelta(days=1)
    )

    target["future_source_timestamp"] = (
        future_source_timestamp
    )

    ground_truth = {
        "anomaly_id": "ANM-000004",
        "entity_type": "MASTERY",
        "entity_id": (
            f"{target['learner_id']}:"
            f"{target['skill_id']}"
        ),
        "issue_type": "FUTURE_MASTERY_LEAKAGE",
        "description": (
            "Mastery intentionally references source "
            "evidence occurring after its as-of cutoff."
        ),
        "mastery_as_of_timestamp": (
            original_as_of_timestamp
        ),
        "future_source_timestamp": (
            future_source_timestamp
        ),
    }

    return modified_mastery, ground_truth