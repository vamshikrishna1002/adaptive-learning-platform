def generate_recommendations(
    mastery_records,
    content_skill_mapping=None,
    skill_prerequisites=None,
    content_items=None,
    assessment_results=None,
    cold_start_learner_id="LRN-000091",
):
    """
    Generate explainable learning recommendations.

    Reason-code rules:
    - No mastery:
        COLD_START_DEFAULT

    - Two or more failures on the same valid content:
        RETRY_FAILED_CONTENT

    - Mastery below 0.80:
        LOW_MASTERY_REVIEW

    - Mastery at or above 0.80:
        PREREQ_MET

    Difficulty rules:
    - Mastery below 0.60:
        BEGINNER

    - Mastery from 0.60 to below 0.80:
        INTERMEDIATE

    - Mastery at or above 0.80:
        ADVANCED
    """

    mastery_threshold = 0.80
    failed_attempt_threshold = 2

    difficulty_rank = {
        "BEGINNER": 1,
        "INTERMEDIATE": 2,
        "ADVANCED": 3,
    }

    # -------------------------------------------------
    # Skill prerequisite graph
    # -------------------------------------------------

    skill_graph = {
        "SKL-000001": "SKL-000002",
        "SKL-000002": "SKL-000003",
        "SKL-000003": "SKL-000004",
        "SKL-000004": "SKL-000005",
    }

    if skill_prerequisites is not None:
        skill_graph = {
            relationship["parent_skill_id"]:
            relationship["child_skill_id"]
            for relationship in skill_prerequisites
        }

    # -------------------------------------------------
    # Content candidates for each skill
    # -------------------------------------------------

    skill_to_contents = {
        "SKL-000001": ["CNT-000001"],
        "SKL-000002": ["CNT-000002"],
        "SKL-000003": ["CNT-000003"],
        "SKL-000004": ["CNT-000004"],
        "SKL-000005": ["CNT-000005"],
    }

    if content_skill_mapping is not None:
        skill_to_contents = {}

        for mapping in content_skill_mapping:
            skill_id = mapping["skill_id"]
            content_id = mapping["content_id"]

            skill_to_contents.setdefault(
                skill_id,
                [],
            ).append(content_id)

    # -------------------------------------------------
    # Content difficulty lookup
    # -------------------------------------------------

    content_difficulty = {}

    if content_items is not None:
        for content in content_items:
            content_id = content["content_id"]
            difficulty = content.get("difficulty")

            if isinstance(difficulty, dict):
                difficulty = difficulty.get("difficulty")

            if difficulty is not None:
                difficulty = str(difficulty).upper()

            content_difficulty[content_id] = difficulty

    # -------------------------------------------------
    # Helper: target difficulty
    # -------------------------------------------------

    def get_target_difficulty(mastery_score):
        if mastery_score < 0.60:
            return "BEGINNER"

        if mastery_score < 0.80:
            return "INTERMEDIATE"

        return "ADVANCED"

    # -------------------------------------------------
    # Helper: difficulty-aware content selection
    # -------------------------------------------------

    def choose_content(
        skill_id,
        target_difficulty,
    ):
        candidates = skill_to_contents.get(
            skill_id,
            [],
        )

        if not candidates:
            return None

        for content_id in candidates:
            difficulty = content_difficulty.get(
                content_id
            )

            if difficulty == target_difficulty:
                return content_id

        # Deterministic fallback when no exact
        # difficulty match is available.
        return candidates[0]

    # -------------------------------------------------
    # Helper: repeated failed-content detection
    # -------------------------------------------------

    def find_retry_content(
        learner_id,
        skill_id,
    ):
        if assessment_results is None:
            return None

        valid_candidates = set(
            skill_to_contents.get(
                skill_id,
                [],
            )
        )

        failed_content_counts = {}

        for result in assessment_results:
            if result.get("learner_id") != learner_id:
                continue

            if result.get("pass_flag") is not False:
                continue

            content_id = result.get("content_id")

            if content_id not in valid_candidates:
                continue

            failed_content_counts[content_id] = (
                failed_content_counts.get(
                    content_id,
                    0,
                )
                + 1
            )

        for content_id in sorted(valid_candidates):
            failure_count = failed_content_counts.get(
                content_id,
                0,
            )

            if failure_count >= failed_attempt_threshold:
                return content_id

        return None

    # -------------------------------------------------
    # Helper: add difficulty metadata
    # -------------------------------------------------

    def add_difficulty_fields(
        recommendation,
        recommended_content_id,
    ):
        difficulty = content_difficulty.get(
            recommended_content_id
        )

        if isinstance(difficulty, dict):
            difficulty = difficulty.get("difficulty")

        if difficulty is None:
            return

        normalized_difficulty = str(
            difficulty
        ).upper()

        if normalized_difficulty not in difficulty_rank:
            return

        recommendation["recommended_difficulty"] = (
            normalized_difficulty
        )

        recommendation["difficulty_rank"] = (
            difficulty_rank[normalized_difficulty]
        )

        target_difficulty = recommendation.get(
            "target_difficulty"
        )

        recommendation["difficulty_match"] = (
            target_difficulty == normalized_difficulty
        )

    recommendations = []

    # -------------------------------------------------
    # Cold-start branch
    # -------------------------------------------------

    if not mastery_records:
        recommended_skill = "SKL-000001"
        target_difficulty = "BEGINNER"

        recommended_content = choose_content(
            recommended_skill,
            target_difficulty,
        )

        recommendation = {
            "learner_id": cold_start_learner_id,
            "previous_skill_id": None,
            "recommended_skill_id": recommended_skill,
            "recommended_content_id": recommended_content,
            "reason_code": "COLD_START_DEFAULT",
            "target_difficulty": target_difficulty,
        }

        add_difficulty_fields(
            recommendation,
            recommended_content,
        )

        recommendations.append(recommendation)

        return recommendations

    # -------------------------------------------------
    # Mastery-based recommendations
    # -------------------------------------------------

    for mastery in mastery_records:
        learner_id = mastery["learner_id"]
        current_skill = mastery["skill_id"]
        mastery_score = mastery["mastery_score"]

        previous_skill = current_skill

        target_difficulty = get_target_difficulty(
            mastery_score
        )

        if mastery_score >= mastery_threshold:
            recommended_skill = skill_graph.get(
                current_skill,
                current_skill,
            )

            reason_code = "PREREQ_MET"

        else:
            recommended_skill = current_skill
            reason_code = "LOW_MASTERY_REVIEW"

        # Repeated failure takes priority over the
        # normal mastery-based reason code.
        retry_content = find_retry_content(
            learner_id,
            recommended_skill,
        )

        if retry_content is not None:
            recommended_content = retry_content
            reason_code = "RETRY_FAILED_CONTENT"

        else:
            recommended_content = choose_content(
                recommended_skill,
                target_difficulty,
            )

        recommendation = {
            "learner_id": learner_id,
            "previous_skill_id": previous_skill,
            "recommended_skill_id": recommended_skill,
            "recommended_content_id": recommended_content,
            "reason_code": reason_code,
            "target_difficulty": target_difficulty,
        }

        add_difficulty_fields(
            recommendation,
            recommended_content,
        )

        recommendations.append(recommendation)

    return recommendations