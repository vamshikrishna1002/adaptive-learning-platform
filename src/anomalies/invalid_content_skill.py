def inject_invalid_content_skill(
    content_skill_mapping
):
    """
    Inject one invalid ContentSkill foreign-key reference.

    The clean source data is copied first so it
    remains unchanged.
    """

    modified_mapping = [
        mapping.copy()
        for mapping in content_skill_mapping
    ]

    if not modified_mapping:
        return modified_mapping, None

    target = modified_mapping[0]

    original_skill_id = target["skill_id"]
    invalid_skill_id = "SKL-999999"

    target["skill_id"] = invalid_skill_id

    ground_truth = {
        "anomaly_id": "ANM-000003",
        "entity_type": "CONTENT_SKILL",
        "entity_id": target["content_id"],
        "issue_type": (
            "INVALID_CONTENT_SKILL_REFERENCE"
        ),
        "description": (
            "ContentSkill intentionally references "
            "a nonexistent skill."
        ),
        "original_skill_id": original_skill_id,
        "anomalous_skill_id": invalid_skill_id,
    }

    return modified_mapping, ground_truth