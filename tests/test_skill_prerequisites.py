from src.generators.skill_prerequisite_generator import (
    generate_skill_prerequisites
)


def test_skill_prerequisite_count():
    prerequisites = generate_skill_prerequisites()

    assert len(prerequisites) == 4


def test_skill_prerequisites_have_no_self_loops():
    prerequisites = generate_skill_prerequisites()

    for relationship in prerequisites:
        assert (
            relationship["parent_skill_id"]
            != relationship["child_skill_id"]
        )
def test_skill_prerequisite_graph_has_no_cycles():
    prerequisites = generate_skill_prerequisites()

    graph = {}

    for relationship in prerequisites:
        parent = relationship["parent_skill_id"]
        child = relationship["child_skill_id"]

        graph.setdefault(parent, []).append(child)

    visiting = set()
    visited = set()

    def has_cycle(skill_id):
        if skill_id in visiting:
            return True

        if skill_id in visited:
            return False

        visiting.add(skill_id)

        for child_id in graph.get(skill_id, []):
            if has_cycle(child_id):
                return True

        visiting.remove(skill_id)
        visited.add(skill_id)

        return False

    all_skill_ids = set(graph.keys())

    for children in graph.values():
        all_skill_ids.update(children)

    for skill_id in all_skill_ids:
        assert not has_cycle(skill_id)
def test_full_scale_skill_prerequisites():
    prerequisites = (
        generate_skill_prerequisites(
            skill_count=500
        )
    )

    assert len(prerequisites) == 499

    assert prerequisites[0] == {
        "parent_skill_id": "SKL-000001",
        "child_skill_id": "SKL-000002",
    }

    assert prerequisites[-1] == {
        "parent_skill_id": "SKL-000499",
        "child_skill_id": "SKL-000500",
    }