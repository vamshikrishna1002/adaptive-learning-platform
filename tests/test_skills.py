from src.generators.skill_generator import generate_skills
from src.generators.content_skill_generator import (
    generate_content_skill_mapping
)

def test_skill_count():
    skills = generate_skills(5)

    assert len(skills) == 5


def test_multiple_content_items_can_map_to_each_skill():
    mappings = generate_content_skill_mapping(
        content_count=15,
        skill_count=5,
    )

    assert len(mappings) == 15

    mappings_by_skill = {}

    for mapping in mappings:
        skill_id = mapping["skill_id"]

        mappings_by_skill.setdefault(
            skill_id,
            []
        ).append(
            mapping["content_id"]
        )

    assert len(mappings_by_skill) == 5

    for content_ids in mappings_by_skill.values():
        assert len(content_ids) == 3

    assert mappings_by_skill["SKL-000001"] == [
        "CNT-000001",
        "CNT-000006",
        "CNT-000011",
    ]
def test_full_scale_content_skill_mapping():
    mappings = generate_content_skill_mapping(
        content_count=2_000,
        skill_count=500,
    )

    assert len(mappings) == 2_000

    skill_ids = {
        mapping["skill_id"]
        for mapping in mappings
    }

    assert len(skill_ids) == 500

    # 2,000 content items / 500 skills
    # gives 4 content items per skill.
    first_skill_content = [
        mapping["content_id"]
        for mapping in mappings
        if mapping["skill_id"] == "SKL-000001"
    ]

    assert first_skill_content == [
        "CNT-000001",
        "CNT-000501",
        "CNT-001001",
        "CNT-001501",
    ]