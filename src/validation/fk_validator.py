def validate_foreign_key(
    child_records,
    child_field,
    parent_records,
    parent_field,
    entity_type,
):
    """
    Validate that child foreign-key values
    exist in the parent dataset.

    Returns:
        list of validation issue dictionaries
    """

    issues = []

    parent_values = {
        record.get(parent_field)
        for record in parent_records
    }

    for record in child_records:
        foreign_key_value = record.get(
            child_field
        )

        if foreign_key_value not in parent_values:
            issues.append(
                {
                    "entity_type": entity_type,
                    "issue_type": (
                        "INVALID_FOREIGN_KEY"
                    ),
                    "field": child_field,
                    "value": foreign_key_value,
                    "parent_field": parent_field,
                }
            )

    return issues