def generate_skill_prerequisites(
    skill_count=5,
):
    """
    Generate a deterministic prerequisite DAG.

    Each skill depends on the previous skill.

    Example:
    SKL-000001 -> SKL-000002
    SKL-000002 -> SKL-000003
    ...
    """

    if skill_count <= 1:
        return []

    prerequisites = []

    for skill_number in range(
        1,
        skill_count
    ):
        parent_skill_id = (
            f"SKL-{skill_number:06d}"
        )

        child_skill_id = (
            f"SKL-{skill_number + 1:06d}"
        )

        prerequisites.append(
            {
                "parent_skill_id":
                    parent_skill_id,

                "child_skill_id":
                    child_skill_id,
            }
        )

    return prerequisites