from src.events.recommendation_generator import generate_recommendations
from src.generators.content_skill_generator import (generate_content_skill_mapping)
from src.events.attempt_generator import generate_attempts
def test_low_mastery_recommends_review():
    mastery_records = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000001",
            "mastery_score": 0.74
        }
    ]

    recommendations = generate_recommendations(mastery_records)

    assert len(recommendations) == 1

    recommendation = recommendations[0]

    assert recommendation["learner_id"] == "LRN-000001"
    assert recommendation["recommended_skill_id"] == "SKL-000001"
    assert recommendation["reason_code"] == "LOW_MASTERY_REVIEW"
    assert (recommendation["recommended_content_id"]== "CNT-000001")

def test_high_mastery_advances_to_next_skill():
    mastery_records = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000001",
            "mastery_score": 0.85
        }
    ]

    recommendations = generate_recommendations(mastery_records)

    assert len(recommendations) == 1

    recommendation = recommendations[0]

    assert recommendation["learner_id"] == "LRN-000001"
    assert recommendation["recommended_skill_id"] == "SKL-000002"
    assert recommendation["reason_code"] == "PREREQ_MET"
    assert (recommendation["recommended_content_id"] == "CNT-000002")

def test_recommended_content_matches_recommended_skill():
    mastery_records = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000001",
            "mastery_score": 0.85
        }
    ]

    recommendations = generate_recommendations(
        mastery_records
    )

    content_skill_mapping = (
        generate_content_skill_mapping()
    )

    valid_pairs = {
        (
            mapping["content_id"],
            mapping["skill_id"]
        )
        for mapping in content_skill_mapping
    }

    recommendation = recommendations[0]

    recommended_pair = (
        recommendation["recommended_content_id"],
        recommendation["recommended_skill_id"]
    )

    assert recommended_pair in valid_pairs
def test_recommendation_uses_provided_content_skill_mapping():
    mastery_records = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000001",
            "mastery_score": 0.74
        }
    ]

    custom_mapping = [
        {
            "content_id": "CNT-009999",
            "skill_id": "SKL-000001"
        }
    ]

    recommendations = generate_recommendations(
        mastery_records,
        custom_mapping
    )

    recommendation = recommendations[0]

    assert (
        recommendation["recommended_content_id"]
        == "CNT-009999"
    )
def test_recommendation_uses_provided_skill_prerequisites():
    mastery_records = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000001",
            "mastery_score": 0.90
        }
    ]

    custom_content_mapping = [
        {
            "content_id": "CNT-000003",
            "skill_id": "SKL-000003"
        }
    ]

    custom_prerequisites = [
        {
            "parent_skill_id": "SKL-000001",
            "child_skill_id": "SKL-000003"
        }
    ]

    recommendations = generate_recommendations(
        mastery_records,
        custom_content_mapping,
        custom_prerequisites
    )

    recommendation = recommendations[0]

    assert (
        recommendation["recommended_skill_id"]
        == "SKL-000003"
    )

    assert (
        recommendation["recommended_content_id"]
        == "CNT-000003"
    )

    assert recommendation["reason_code"] == "PREREQ_MET"
def test_cold_start_recommendation():
    mastery_records = []

    content_skill_mapping = [
        {
            "content_id": "CNT-000001",
            "skill_id": "SKL-000001"
        }
    ]

    recommendations = generate_recommendations(
        mastery_records,
        content_skill_mapping
    )

    assert len(recommendations) == 1

    recommendation = recommendations[0]

    assert recommendation["learner_id"] == "LRN-000091"

    assert (
        recommendation["recommended_skill_id"]
        == "SKL-000001"
    )

    assert (
        recommendation["recommended_content_id"]
        == "CNT-000001"
    )

    assert (
        recommendation["reason_code"]
        == "COLD_START_DEFAULT"
    )


def test_custom_cold_start_learner_id():
    mastery_records = []

    content_skill_mapping = [
        {
            "content_id": "CNT-000001",
            "skill_id": "SKL-000001"
        }
    ]

    recommendations = generate_recommendations(
        mastery_records,
        content_skill_mapping,
        cold_start_learner_id="LRN-000100"
    )

    assert len(recommendations) == 1

    recommendation = recommendations[0]

    assert recommendation["learner_id"] == "LRN-000100"

    assert (
        recommendation["recommended_skill_id"]
        == "SKL-000001"
    )

    assert (
        recommendation["recommended_content_id"]
        == "CNT-000001"
    )

    assert (
        recommendation["reason_code"]
        == "COLD_START_DEFAULT"
    )
    
def test_cold_start_learner_has_no_attempt_history():
    cold_start_learner_id = "LRN-000091"

    attempts = generate_attempts(
        count=500,
        content_count=5,
        learner_count=90
    )

    learner_attempts = [
        attempt
        for attempt in attempts
        if attempt["learner_id"] == cold_start_learner_id
    ]

    assert learner_attempts == []

    recommendations = generate_recommendations(
        mastery_records=[],
        content_skill_mapping=[
            {
                "content_id": "CNT-000001",
                "skill_id": "SKL-000001"
            }
        ],
        cold_start_learner_id=cold_start_learner_id
    )

    assert recommendations[0]["learner_id"] == cold_start_learner_id
    assert recommendations[0]["reason_code"] == "COLD_START_DEFAULT"
def test_recommendations_for_multiple_mastery_records():
    mastery_records = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000001",
            "mastery_score": 0.55,
        },
        {
            "learner_id": "LRN-000002",
            "skill_id": "SKL-000002",
            "mastery_score": 0.68,
        },
        {
            "learner_id": "LRN-000003",
            "skill_id": "SKL-000003",
            "mastery_score": 0.74,
        },
    ]

    content_skill_mapping = [
        {
            "content_id": "CNT-000001",
            "skill_id": "SKL-000001",
        },
        {
            "content_id": "CNT-000002",
            "skill_id": "SKL-000002",
        },
        {
            "content_id": "CNT-000003",
            "skill_id": "SKL-000003",
        },
    ]

    recommendations = generate_recommendations(
        mastery_records=mastery_records,
        content_skill_mapping=content_skill_mapping,
    )

    assert len(recommendations) == 3

    recommendation_lookup = {
        recommendation["learner_id"]: recommendation
        for recommendation in recommendations
    }

    assert (
        recommendation_lookup["LRN-000001"][
            "recommended_skill_id"
        ]
        == "SKL-000001"
    )

    assert (
        recommendation_lookup["LRN-000001"][
            "recommended_content_id"
        ]
        == "CNT-000001"
    )

    assert (
        recommendation_lookup["LRN-000002"][
            "recommended_skill_id"
        ]
        == "SKL-000002"
    )

    assert (
        recommendation_lookup["LRN-000002"][
            "recommended_content_id"
        ]
        == "CNT-000002"
    )

    assert (
        recommendation_lookup["LRN-000003"][
            "recommended_skill_id"
        ]
        == "SKL-000003"
    )

    assert (
        recommendation_lookup["LRN-000003"][
            "recommended_content_id"
        ]
        == "CNT-000003"
    )

    assert all(
        recommendation["reason_code"]
        == "LOW_MASTERY_REVIEW"
        for recommendation in recommendations
    )
def test_recommendation_count_matches_mastery_count():
    mastery_records = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000001",
            "mastery_score": 0.55,
        },
        {
            "learner_id": "LRN-000002",
            "skill_id": "SKL-000002",
            "mastery_score": 0.68,
        },
        {
            "learner_id": "LRN-000003",
            "skill_id": "SKL-000003",
            "mastery_score": 0.74,
        },
    ]

    content_skill_mapping = [
        {
            "content_id": "CNT-000001",
            "skill_id": "SKL-000001",
        },
        {
            "content_id": "CNT-000002",
            "skill_id": "SKL-000002",
        },
        {
            "content_id": "CNT-000003",
            "skill_id": "SKL-000003",
        },
    ]

    recommendations = generate_recommendations(
        mastery_records=mastery_records,
        content_skill_mapping=content_skill_mapping,
    )

    assert len(recommendations) == len(mastery_records)
def test_recommendation_includes_content_difficulty():
    mastery_records = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000001",
            "mastery_score": 0.55,
        }
    ]

    content_skill_mapping = [
        {
            "content_id": "CNT-000001",
            "skill_id": "SKL-000001",
        }
    ]

    content_items = [
        {
            "content_id": "CNT-000001",
            "content_title": "Python Review",
            "content_type": "VIDEO",
            "difficulty": "ADVANCED",
        }
    ]

    recommendations = generate_recommendations(
        mastery_records=mastery_records,
        content_skill_mapping=content_skill_mapping,
        content_items=content_items,
    )

    recommendation = recommendations[0]

    assert (
        recommendation["recommended_difficulty"]
        == "ADVANCED"
    )

    assert recommendation["difficulty_rank"] == 3
def test_content_difficulty_ranking():
    difficulty_cases = [
        ("BEGINNER", 1),
        ("INTERMEDIATE", 2),
        ("ADVANCED", 3),
    ]

    for difficulty, expected_rank in difficulty_cases:
        mastery_records = [
            {
                "learner_id": "LRN-000001",
                "skill_id": "SKL-000001",
                "mastery_score": 0.55,
            }
        ]

        content_skill_mapping = [
            {
                "content_id": "CNT-000001",
                "skill_id": "SKL-000001",
            }
        ]

        content_items = [
            {
                "content_id": "CNT-000001",
                "content_title": "Python Review",
                "content_type": "VIDEO",
                "difficulty": difficulty,
            }
        ]

        recommendations = generate_recommendations(
            mastery_records=mastery_records,
            content_skill_mapping=content_skill_mapping,
            content_items=content_items,
        )

        recommendation = recommendations[0]

        assert (
            recommendation["recommended_difficulty"]
            == difficulty
        )

        assert (
            recommendation["difficulty_rank"]
            == expected_rank
        )
def test_target_difficulty_is_based_on_mastery():
    test_cases = [
        (0.55, "BEGINNER"),
        (0.68, "INTERMEDIATE"),
        (0.79, "INTERMEDIATE"),
        (0.80, "ADVANCED"),
        (0.90, "ADVANCED"),
    ]

    content_skill_mapping = [
        {
            "content_id": "CNT-000001",
            "skill_id": "SKL-000001",
        },
        {
            "content_id": "CNT-000002",
            "skill_id": "SKL-000002",
        },
    ]

    for mastery_score, expected_difficulty in test_cases:
        mastery_records = [
            {
                "learner_id": "LRN-000001",
                "skill_id": "SKL-000001",
                "mastery_score": mastery_score,
            }
        ]

        recommendations = generate_recommendations(
            mastery_records=mastery_records,
            content_skill_mapping=content_skill_mapping,
        )

        recommendation = recommendations[0]

        assert (
            recommendation["target_difficulty"]
            == expected_difficulty
        )
def test_difficulty_match_flag():
    mastery_records = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000001",
            "mastery_score": 0.55,
        }
    ]

    content_skill_mapping = [
        {
            "content_id": "CNT-000001",
            "skill_id": "SKL-000001",
        }
    ]

    beginner_content = [
        {
            "content_id": "CNT-000001",
            "content_title": "Python Beginner Review",
            "content_type": "VIDEO",
            "difficulty": "BEGINNER",
        }
    ]

    matching_recommendations = generate_recommendations(
        mastery_records=mastery_records,
        content_skill_mapping=content_skill_mapping,
        content_items=beginner_content,
    )

    assert (
        matching_recommendations[0]["difficulty_match"]
        is True
    )

    advanced_content = [
        {
            "content_id": "CNT-000001",
            "content_title": "Python Advanced Review",
            "content_type": "PROJECT",
            "difficulty": "ADVANCED",
        }
    ]

    mismatching_recommendations = generate_recommendations(
        mastery_records=mastery_records,
        content_skill_mapping=content_skill_mapping,
        content_items=advanced_content,
    )

    assert (
        mismatching_recommendations[0]["difficulty_match"]
        is False
    )
def test_difficulty_match_flag():
    mastery_records = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000001",
            "mastery_score": 0.55,
        }
    ]

    content_skill_mapping = [
        {
            "content_id": "CNT-000001",
            "skill_id": "SKL-000001",
        }
    ]

    # 0.55 mastery targets BEGINNER.
    beginner_content = [
        {
            "content_id": "CNT-000001",
            "content_title": "Python Basics",
            "content_type": "VIDEO",
            "difficulty": "BEGINNER",
        }
    ]

    recommendations = generate_recommendations(
        mastery_records=mastery_records,
        content_skill_mapping=content_skill_mapping,
        content_items=beginner_content,
    )

    assert recommendations[0]["target_difficulty"] == "BEGINNER"
    assert recommendations[0]["recommended_difficulty"] == "BEGINNER"
    assert recommendations[0]["difficulty_match"] is True

    advanced_content = [
        {
            "content_id": "CNT-000001",
            "content_title": "Python Advanced",
            "content_type": "VIDEO",
            "difficulty": "ADVANCED",
        }
    ]

    recommendations = generate_recommendations(
        mastery_records=mastery_records,
        content_skill_mapping=content_skill_mapping,
        content_items=advanced_content,
    )

    assert recommendations[0]["target_difficulty"] == "BEGINNER"
    assert recommendations[0]["recommended_difficulty"] == "ADVANCED"
    assert recommendations[0]["difficulty_match"] is False
def test_selects_content_matching_target_difficulty():
    mastery_records = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000001",
            "mastery_score": 0.55,
        }
    ]

    # Three content items teach the same skill.
    content_skill_mapping = [
        {
            "content_id": "CNT-000001",
            "skill_id": "SKL-000001",
        },
        {
            "content_id": "CNT-000006",
            "skill_id": "SKL-000001",
        },
        {
            "content_id": "CNT-000011",
            "skill_id": "SKL-000001",
        },
    ]

    content_items = [
        {
            "content_id": "CNT-000001",
            "content_title": "Advanced Python",
            "content_type": "PROJECT",
            "difficulty": "ADVANCED",
        },
        {
            "content_id": "CNT-000006",
            "content_title": "Intermediate Python",
            "content_type": "LAB",
            "difficulty": "INTERMEDIATE",
        },
        {
            "content_id": "CNT-000011",
            "content_title": "Python Introduction",
            "content_type": "VIDEO",
            "difficulty": "BEGINNER",
        },
    ]

    recommendations = generate_recommendations(
        mastery_records=mastery_records,
        content_skill_mapping=content_skill_mapping,
        content_items=content_items,
    )

    recommendation = recommendations[0]

    assert recommendation["target_difficulty"] == "BEGINNER"

    assert (
        recommendation["recommended_content_id"]
        == "CNT-000011"
    )

    assert (
        recommendation["recommended_difficulty"]
        == "BEGINNER"
    )

    assert recommendation["difficulty_rank"] == 1
    assert recommendation["difficulty_match"] is True
def test_selects_intermediate_content_for_medium_mastery():
    mastery_records = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000001",
            "mastery_score": 0.68,
        }
    ]

    content_skill_mapping = [
        {
            "content_id": "CNT-000001",
            "skill_id": "SKL-000001",
        },
        {
            "content_id": "CNT-000006",
            "skill_id": "SKL-000001",
        },
        {
            "content_id": "CNT-000011",
            "skill_id": "SKL-000001",
        },
    ]

    content_items = [
        {
            "content_id": "CNT-000001",
            "difficulty": "ADVANCED",
        },
        {
            "content_id": "CNT-000006",
            "difficulty": "INTERMEDIATE",
        },
        {
            "content_id": "CNT-000011",
            "difficulty": "BEGINNER",
        },
    ]

    recommendations = generate_recommendations(
        mastery_records=mastery_records,
        content_skill_mapping=content_skill_mapping,
        content_items=content_items,
    )

    recommendation = recommendations[0]

    assert (
        recommendation["target_difficulty"]
        == "INTERMEDIATE"
    )

    assert (
        recommendation["recommended_content_id"]
        == "CNT-000006"
    )

    assert (
        recommendation["recommended_difficulty"]
        == "INTERMEDIATE"
    )

    assert recommendation["difficulty_match"] is True
def test_high_mastery_selects_advanced_content():
    mastery_records = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000001",
            "mastery_score": 0.85,
        }
    ]

    skill_prerequisites = [
        {
            "parent_skill_id": "SKL-000001",
            "child_skill_id": "SKL-000002",
        }
    ]

    content_skill_mapping = [
        {
            "content_id": "CNT-000002",
            "skill_id": "SKL-000002",
        },
        {
            "content_id": "CNT-000007",
            "skill_id": "SKL-000002",
        },
        {
            "content_id": "CNT-000012",
            "skill_id": "SKL-000002",
        },
    ]

    content_items = [
        {
            "content_id": "CNT-000002",
            "difficulty": "BEGINNER",
        },
        {
            "content_id": "CNT-000007",
            "difficulty": "INTERMEDIATE",
        },
        {
            "content_id": "CNT-000012",
            "difficulty": "ADVANCED",
        },
    ]

    recommendations = generate_recommendations(
        mastery_records=mastery_records,
        content_skill_mapping=content_skill_mapping,
        skill_prerequisites=skill_prerequisites,
        content_items=content_items,
    )

    recommendation = recommendations[0]

    assert recommendation["previous_skill_id"] == "SKL-000001"
    assert recommendation["recommended_skill_id"] == "SKL-000002"
    assert recommendation["reason_code"] == "PREREQ_MET"
    assert recommendation["target_difficulty"] == "ADVANCED"

    assert (
        recommendation["recommended_content_id"]
        == "CNT-000012"
    )

    assert (
        recommendation["recommended_difficulty"]
        == "ADVANCED"
    )

    assert recommendation["difficulty_match"] is True
def test_final_skill_does_not_advance_past_graph():
    mastery_records = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000005",
            "mastery_score": 0.90,
        }
    ]

    content_skill_mapping = [
        {
            "content_id": "CNT-000005",
            "skill_id": "SKL-000005",
        }
    ]

    content_items = [
        {
            "content_id": "CNT-000005",
            "difficulty": "ADVANCED",
        }
    ]

    recommendations = generate_recommendations(
        mastery_records=mastery_records,
        content_skill_mapping=content_skill_mapping,
        content_items=content_items,
    )

    recommendation = recommendations[0]

    assert (
        recommendation["recommended_skill_id"]
        == "SKL-000005"
    )

    assert (
        recommendation["recommended_content_id"]
        == "CNT-000005"
    )

    assert recommendation["target_difficulty"] == "ADVANCED"

    assert "SKL-000006" not in str(recommendation)
def test_difficulty_fallback_when_exact_match_missing():
    mastery_records = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000001",
            "mastery_score": 0.55,
        }
    ]

    content_skill_mapping = [
        {
            "content_id": "CNT-000001",
            "skill_id": "SKL-000001",
        },
        {
            "content_id": "CNT-000006",
            "skill_id": "SKL-000001",
        },
    ]

    content_items = [
        {
            "content_id": "CNT-000001",
            "difficulty": "ADVANCED",
        },
        {
            "content_id": "CNT-000006",
            "difficulty": "INTERMEDIATE",
        },
    ]

    recommendations = generate_recommendations(
        mastery_records=mastery_records,
        content_skill_mapping=content_skill_mapping,
        content_items=content_items,
    )

    recommendation = recommendations[0]

    # Mastery 0.55 targets BEGINNER.
    assert (
        recommendation["target_difficulty"]
        == "BEGINNER"
    )

    # No BEGINNER content exists, so use
    # the first deterministic fallback.
    assert (
        recommendation["recommended_content_id"]
        == "CNT-000001"
    )

    assert (
        recommendation["recommended_difficulty"]
        == "ADVANCED"
    )

    assert recommendation["difficulty_match"] is False
def test_retry_failed_content_reason_code():
    mastery_records = [
        {
            "learner_id": "LRN-000001",
            "skill_id": "SKL-000001",
            "mastery_score": 0.40,
        }
    ]

    content_skill_mapping = [
        {
            "content_id": "CNT-000001",
            "skill_id": "SKL-000001",
        }
    ]

    assessment_results = [
        {
            "attempt_id": "ATT-001",
            "learner_id": "LRN-000001",
            "content_id": "CNT-000001",
            "score": 40,
            "pass_flag": False,
        },
        {
            "attempt_id": "ATT-002",
            "learner_id": "LRN-000001",
            "content_id": "CNT-000001",
            "score": 45,
            "pass_flag": False,
        },
    ]

    recommendations = generate_recommendations(
        mastery_records=mastery_records,
        content_skill_mapping=content_skill_mapping,
        assessment_results=assessment_results,
    )

    recommendation = recommendations[0]

    assert (
        recommendation["reason_code"]
        == "RETRY_FAILED_CONTENT"
    )

    assert (
        recommendation["recommended_content_id"]
        == "CNT-000001"
    )
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

    Rules:
    - No mastery:
        Recommend the entry skill using COLD_START_DEFAULT.

    - Two or more failures on the same content:
        Recommend that content using RETRY_FAILED_CONTENT.

    - Mastery below 0.80:
        Review the current skill.

    - Mastery at or above 0.80:
        Advance to the next skill in the prerequisite graph.

    - Recommended content must map to the recommended skill.

    - Target difficulty:
        mastery < 0.60  -> BEGINNER
        mastery < 0.80  -> INTERMEDIATE
        mastery >= 0.80 -> ADVANCED

    - When multiple content items teach the same skill,
      prefer content matching the learner's target difficulty.
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

        return candidates[0]

    # -------------------------------------------------
    # Helper: repeated failed-content lookup
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
            if (
                failed_content_counts.get(content_id, 0)
                >= failed_attempt_threshold
            ):
                return content_id

        return None

    # -------------------------------------------------
    # Helper: difficulty metadata
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
    # Cold-start recommendation
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

