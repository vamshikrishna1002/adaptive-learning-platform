def validate_primary_key_uniqueness(
    records,
    key_field,
    entity_type,
):
    """
    Validate that every primary-key value is unique.

    Returns:
        list of validation issue records
    """

    issues = []
    seen_ids = set()

    for record in records:
        key_value = record.get(key_field)

        if key_value in seen_ids:
            issues.append(
                {
                    "entity_type": entity_type,
                    "issue_type": "DUPLICATE_PRIMARY_KEY",
                    "field": key_field,
                    "value": key_value,
                }
            )
        else:
            seen_ids.add(key_value)

    return issues