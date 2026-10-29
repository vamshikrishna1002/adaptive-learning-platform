def calculate_metrics(
    learners,
    assessment_results,
    recommendations,
    validation_issues=None,
):
    """
    Calculate summary metrics for the
    adaptive learning platform.
    """

    if validation_issues is None:
        validation_issues = []

    total_learners = len(learners)

    total_assessments = len(
        assessment_results
    )

    total_recommendations = len(
        recommendations
    )

    # ---------------------------------------------
    # Recommendation coverage
    # ---------------------------------------------

    learners_with_recommendations = {
        recommendation["learner_id"]
        for recommendation in recommendations
    }

    if total_learners > 0:
        recommendation_coverage = (
            len(learners_with_recommendations)
            / total_learners
        )
    else:
        recommendation_coverage = 0.0

    # ---------------------------------------------
    # Assessment pass rate
    # ---------------------------------------------

    passed_assessments = sum(
        1
        for result in assessment_results
        if result.get("pass_flag") is True
    )

    if total_assessments > 0:
        pass_rate = (
            passed_assessments
            / total_assessments
        )
    else:
        pass_rate = 0.0

    # ---------------------------------------------
    # Difficulty match rate
    # ---------------------------------------------

    difficulty_records = [
        recommendation
        for recommendation in recommendations
        if "difficulty_match" in recommendation
    ]

    difficulty_matches = sum(
        1
        for recommendation in difficulty_records
        if recommendation["difficulty_match"] is True
    )

    if difficulty_records:
        difficulty_match_rate = (
            difficulty_matches
            / len(difficulty_records)
        )
    else:
        difficulty_match_rate = 0.0

    # ---------------------------------------------
    # Cold-start recommendation rate
    # ---------------------------------------------

    cold_start_count = sum(
        1
        for recommendation in recommendations
        if recommendation.get("reason_code")
        == "COLD_START_DEFAULT"
    )

    if total_recommendations > 0:
        cold_start_rate = (
            cold_start_count
            / total_recommendations
        )
    else:
        cold_start_rate = 0.0

    # ---------------------------------------------
    # Prerequisite violation rate
    # ---------------------------------------------

    prerequisite_violations = sum(
        1
        for issue in validation_issues
        if issue.get("issue_type")
        == "PREREQUISITE_VIOLATION"
    )

    if total_recommendations > 0:
        prerequisite_violation_rate = (
            prerequisite_violations
            / total_recommendations
        )
    else:
        prerequisite_violation_rate = 0.0

    return {
        "total_learners": total_learners,
        "total_assessments": total_assessments,
        "total_recommendations": (
            total_recommendations
        ),
        "recommendation_coverage": round(
            recommendation_coverage,
            4,
        ),
        "pass_rate": round(
            pass_rate,
            4,
        ),
        "difficulty_match_rate": round(
            difficulty_match_rate,
            4,
        ),
        "cold_start_rate": round(
            cold_start_rate,
            4,
        ),
        "prerequisite_violation_rate": round(
            prerequisite_violation_rate,
            4,
        ),
    }