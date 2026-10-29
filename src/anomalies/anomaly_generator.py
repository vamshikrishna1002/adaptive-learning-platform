def create_ground_truth_record(
    anomaly_id,
    entity_type,
    entity_id,
    issue_type,
    description,
):
    """
    Create one ground-truth anomaly record.

    Ground truth is stored separately from the
    clean recommendation/generation inputs.
    """

    return {
        "anomaly_id": anomaly_id,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "issue_type": issue_type,
        "description": description,
    }