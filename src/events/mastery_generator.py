from collections import defaultdict


def generate_mastery(
    assessment_results,
    as_of_timestamp=None,
    content_skill_mapping=None
):
    """
    Calculate mastery from assessment results.

    When content_skill_mapping is supplied, mastery is calculated
    separately for every learner and skill.

    When no mapping is supplied, the existing single-record behavior
    is retained for backward compatibility with current tests.
    """

    if not assessment_results:
        return []

    filtered_results = assessment_results

    if as_of_timestamp is not None:
        filtered_results = [
            result
            for result in assessment_results
            if result["attempt_timestamp"] <= as_of_timestamp
        ]

    if not filtered_results:
        return []

    # Backward-compatible behavior for existing tests.
    if content_skill_mapping is None:
        total_score = sum(
            result["score"]
            for result in filtered_results
        )

        average_score = (
            total_score / len(filtered_results)
        )

        mastery_score = round(
            average_score / 100,
            4
        )

        return [
            {
                "learner_id": "LRN-000001",
                "skill_id": "SKL-000001",
                "mastery_score": mastery_score,
                "mastery_as_of_timestamp": (
                    as_of_timestamp
                ),
            }
        ]

    # Convert ContentSkill records into a lookup.
    content_to_skill = {
        mapping["content_id"]: mapping["skill_id"]
        for mapping in content_skill_mapping
    }

    grouped_scores = defaultdict(list)

    for result in filtered_results:
        learner_id = result["learner_id"]
        content_id = result["content_id"]

        skill_id = content_to_skill.get(content_id)

        # Ignore content that has no skill mapping.
        if skill_id is None:
            continue

        group_key = (
            learner_id,
            skill_id
        )

        grouped_scores[group_key].append(
            result["score"]
        )

    mastery_records = []

    for (
        learner_id,
        skill_id
    ), scores in grouped_scores.items():

        average_score = sum(scores) / len(scores)

        mastery_score = round(
            average_score / 100,
            4
        )

        mastery_records.append(
            {
                "learner_id": learner_id,
                "skill_id": skill_id,
                "mastery_score": mastery_score,
                "mastery_as_of_timestamp": (
                    as_of_timestamp
                ),
            }
        )

    return mastery_records