def generate_assessment_results(attempts):
    """
    Generate one assessment result for every attempt.

    Rules:
    - Every result references a real attempt.
    - Score generation is deterministic.
    - pass_flag is derived from score.
    - Learner, content, and timestamp lineage are preserved.
    """

    results = []

    base_scores = [55, 68, 74, 82, 91]

    for index, attempt in enumerate(attempts):
        score = base_scores[index % len(base_scores)]

        results.append(
            {
                "attempt_id": attempt["attempt_id"],
                "learner_id": attempt["learner_id"],
                "content_id": attempt["content_id"],
                "score": score,
                "pass_flag": score >= 60,
                "attempt_timestamp": attempt[
                    "attempt_timestamp"
                ],
            }
        )

    return results