def validate_enum_values(
    records,
    field,
    allowed_values,
    entity_type,
):
    """
    Detect values outside the permitted enum set.
    """

    issues = []

    for record in records:
        value = record.get(field)

        if value not in allowed_values:
            issues.append(
                {
                    "entity_type": entity_type,
                    "issue_type": "INVALID_ENUM_VALUE",
                    "field": field,
                    "value": value,
                }
            )

    return issues