def validate_duplicates(
    records,
    fields,
    entity_type,
):
    """
    Detect duplicate records based on selected fields.
    """

    issues = []
    seen_values = set()

    for record in records:
        duplicate_key = tuple(
            record.get(field)
            for field in fields
        )

        if duplicate_key in seen_values:
            issues.append(
                {
                    "entity_type": entity_type,
                    "issue_type": "DUPLICATE_RECORD",
                    "fields": fields,
                    "values": duplicate_key,
                }
            )
        else:
            seen_values.add(duplicate_key)

    return issues