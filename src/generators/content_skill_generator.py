def generate_content_skill_mapping(
    content_count=5,
    skill_count=5,
):
    """
    Map generated content items to generated skills.

    Content is assigned to skills in round-robin order.

    Examples:
    - 5 content items and 5 skills:
      one content item per skill.

    - 15 content items and 5 skills:
      three content items per skill.
    """

    if content_count < 1:
        return []

    if skill_count < 1:
        return []

    mappings = []

    for content_number in range(
        1,
        content_count + 1
    ):
        skill_number = (
            (content_number - 1) % skill_count
        ) + 1

        mappings.append(
            {
                "content_id": (
                    f"CNT-{content_number:06d}"
                ),
                "skill_id": (
                    f"SKL-{skill_number:06d}"
                ),
            }
        )

    return mappings