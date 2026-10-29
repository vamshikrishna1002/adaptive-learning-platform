def generate_skills(count=5):
    """
    Generate skill records.

    The first five skills preserve the named
    starter learning path. Additional skills use
    deterministic scalable names.
    """

    if count < 1:
        return []

    base_skill_names = [
        "Python Basics",
        "SQL Fundamentals",
        "Data Analysis",
        "Machine Learning Basics",
        "Deep Learning",
    ]

    skills = []

    for skill_number in range(
        1,
        count + 1,
    ):
        if skill_number <= len(base_skill_names):
            skill_name = base_skill_names[
                skill_number - 1
            ]
        else:
            skill_name = (
                f"Advanced Learning Skill "
                f"{skill_number:03d}"
            )

        skills.append(
            {
                "skill_id": (
                    f"SKL-{skill_number:06d}"
                ),
                "skill_name": skill_name,
            }
        )

    return skills