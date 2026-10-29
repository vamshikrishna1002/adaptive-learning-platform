from datetime import datetime
import random
from src.exporters_json import (
    save_json,
)
import numpy as np
import pandas as pd
import json
from src.reproducibility.manifest import (
    create_checksum_manifest,
)
from src.metrics.metrics_calculator import (
    calculate_metrics,
)
from config.settings import (
    SEED,
    STARTER_SCALE,
    FULL_SCALE,
)

from src.exporters import save_csv

from src.validation.validation_runner import (
    run_validation,
)
from src.validation.validation_exporter import (
    export_validation_summary,
)

from src.generators.learner_generator import (
    generate_learners,
)
from src.generators.course_generator import (
    generate_courses,
)
from src.generators.skill_generator import (
    generate_skills,
)
from src.generators.skill_prerequisite_generator import (
    generate_skill_prerequisites,
)
from src.generators.content_generator import (
    generate_content_items,
)
from src.generators.content_skill_generator import (
    generate_content_skill_mapping,
)

from src.events.attempt_generator import (
    generate_attempts,
)
from src.events.assessment_result_generator import (
    generate_assessment_results,
)
from src.events.mastery_generator import (
    generate_mastery,
)
from src.events.recommendation_generator import (
    generate_recommendations,
)
from src.events.learning_path_generator import (
    generate_learning_paths,
)

from src.anomalies.prerequisite_violation import (
    inject_prerequisite_violation,
)
from src.anomalies.invalid_attempt_timestamp import (
    inject_invalid_attempt_timestamp,
)
from src.anomalies.invalid_content_skill import (
    inject_invalid_content_skill,
)
from src.anomalies.future_mastery_leakage import (
    inject_future_mastery_leakage,
)
from src.anomalies.learning_path_loop import (
    inject_learning_path_loop,
)
from src.anomalies.ground_truth_exporter import (
    export_ground_truth,
)


# -----------------------------------------------------
# RANDOM SEED
# -----------------------------------------------------

random.seed(SEED)
np.random.seed(SEED)


# -----------------------------------------------------
# SCALE
# -----------------------------------------------------

# Use STARTER_SCALE during development.
# Change to FULL_SCALE for final large-scale generation.
SCALE = FULL_SCALE


def main():

    print("=" * 60)
    print("Adaptive Learning Platform Generator")
    print("=" * 60)

    print(f"Seed: {SEED}")
    print(f"Scale: {SCALE}")
    print()

    # -------------------------------------------------
    # 1. LEARNERS
    # -------------------------------------------------

    learners = generate_learners(
        SCALE["learners"]
    )

    learners_df = pd.DataFrame(
        learners
    )

    save_csv(
        learners_df,
        "data/output/learners.csv",
    )

    print("\nLearners Preview:\n")
    print(learners_df.head())

    print(
        f"\nTotal learners generated: "
        f"{len(learners)}"
    )

    # -------------------------------------------------
    # 2. COURSES
    # -------------------------------------------------

    courses = generate_courses(5)

    courses_df = pd.DataFrame(
        courses
    )

    save_csv(
        courses_df,
        "data/output/courses.csv",
    )

    print("\nCourses Preview:\n")

    for course in courses[:5]:
        print(course)

    print(
        f"\nTotal courses generated: "
        f"{len(courses)}"
    )

    # -------------------------------------------------
    # 3. SKILLS
    # -------------------------------------------------

    skills = generate_skills(
        SCALE["skills"]
    )

    skills_df = pd.DataFrame(
        skills
    )

    save_csv(
        skills_df,
        "data/output/skills.csv",
    )

    print("\nSkills Preview:\n")

    for skill in skills[:10]:
        print(skill)

    print(
        f"\nTotal skills generated: "
        f"{len(skills)}"
    )

    # -------------------------------------------------
    # 4. SKILL PREREQUISITES
    # -------------------------------------------------

    skill_prerequisites = (
    generate_skill_prerequisites(
        skill_count=SCALE["skills"]
    )
)

    skill_prerequisites_df = pd.DataFrame(
        skill_prerequisites
    )

    save_csv(
        skill_prerequisites_df,
        "data/output/skill_prerequisites.csv",
    )

    print("\nSkill Prerequisites Preview:\n")

    for relationship in skill_prerequisites[:10]:
        print(relationship)

    print(
        f"\nTotal prerequisite relationships: "
        f"{len(skill_prerequisites)}"
    )

    # -------------------------------------------------
    # 5. CONTENT ITEMS
    # -------------------------------------------------

    content_items = generate_content_items(
        SCALE["content_items"]
    )

    content_items_df = pd.DataFrame(
        content_items
    )

    save_csv(
        content_items_df,
        "data/output/content_items.csv",
    )

    print("\nContent Items Preview:\n")

    for content in content_items[:10]:
        print(content)

    print(
        f"\nTotal content items generated: "
        f"{len(content_items)}"
    )

    # -------------------------------------------------
    # 6. CONTENT-SKILL MAPPING
    # -------------------------------------------------

    content_skill_mapping = (
        generate_content_skill_mapping(
            content_count=SCALE["content_items"],
            skill_count=SCALE["skills"],
        )
    )

    content_skill_df = pd.DataFrame(
        content_skill_mapping
    )

    save_csv(
        content_skill_df,
        "data/output/content_skill.csv",
    )

    print("\nContent-Skill Mapping Preview:\n")

    for mapping in content_skill_mapping[:10]:
        print(mapping)

    print(
        f"\nTotal content-skill mappings: "
        f"{len(content_skill_mapping)}"
    )

    # -------------------------------------------------
    # 7. ATTEMPTS
    # -------------------------------------------------

    # Reserve 10% of learners as cold-start learners.
    active_learner_count = int(
        SCALE["learners"] * 0.90
    )

    attempts = generate_attempts(
        count=SCALE["attempts"],
        content_count=SCALE["content_items"],
        learner_count=active_learner_count,
    )

    attempts_df = pd.DataFrame(
        attempts
    )

    save_csv(
        attempts_df,
        "data/output/attempts.csv",
    )

    print("\nAttempts Preview:\n")

    for attempt in attempts[:5]:
        print(attempt)

    print(
        f"\nTotal attempts generated: "
        f"{len(attempts)}"
    )

    print(
        f"Active learners with possible attempts: "
        f"{active_learner_count}"
    )

    print(
        f"Cold-start learners reserved: "
        f"{SCALE['learners'] - active_learner_count}"
    )

    # -------------------------------------------------
    # 8. ASSESSMENT RESULTS
    # -------------------------------------------------

    assessment_results = (
        generate_assessment_results(
            attempts
        )
    )

    assessment_results_df = pd.DataFrame(
        assessment_results
    )

    save_csv(
        assessment_results_df,
        "data/output/assessment_results.csv",
    )

    print("\nAssessment Results Preview:\n")

    for result in assessment_results[:5]:
        print(result)

    print(
        f"\nTotal assessment results generated: "
        f"{len(assessment_results)}"
    )

    # -------------------------------------------------
    # 9. MASTERY
    # -------------------------------------------------

    # Temporal cutoff prevents future-data leakage.
    if assessment_results:
        mastery_as_of_timestamp = max(
        result["attempt_timestamp"]
        for result in assessment_results
    )
    else:
        mastery_as_of_timestamp = datetime(
        2026,
        1,
        1,
        0,
        0,
        0,
    )

    mastery_records = generate_mastery(
        assessment_results,
        as_of_timestamp=mastery_as_of_timestamp,
        content_skill_mapping=content_skill_mapping,
    )

    mastery_df = pd.DataFrame(
        mastery_records
    )

    save_csv(
        mastery_df,
        "data/output/mastery.csv",
    )

    print("\nMastery Records Preview:\n")

    for mastery in mastery_records[:10]:
        print(mastery)

    print(
        f"\nTotal mastery records generated: "
        f"{len(mastery_records)}"
    )

    # -------------------------------------------------
    # 10. MASTERY-BASED RECOMMENDATIONS
    # -------------------------------------------------

    recommendations = generate_recommendations(
        mastery_records=mastery_records,
        content_skill_mapping=content_skill_mapping,
        skill_prerequisites=skill_prerequisites,
        content_items=content_items,
        assessment_results=assessment_results,
    )

    # -------------------------------------------------
    # 11. COLD-START RECOMMENDATION
    # -------------------------------------------------

    first_cold_start_number = (
        active_learner_count + 1
    )

    cold_start_learner_id = (
        f"LRN-{first_cold_start_number:06d}"
    )

    cold_start_recommendations = (
        generate_recommendations(
            mastery_records=[],
            content_skill_mapping=content_skill_mapping,
            skill_prerequisites=skill_prerequisites,
            content_items=content_items,
            assessment_results=assessment_results,
            cold_start_learner_id=(
                cold_start_learner_id
            ),
        )
    )

    recommendations.extend(
        cold_start_recommendations
    )

    recommendations_df = pd.DataFrame(
        recommendations
    )

    save_csv(
        recommendations_df,
        "data/output/recommendations.csv",
    )

    print("\nRecommendations Preview:\n")

    for recommendation in recommendations[:10]:
        print(recommendation)

    print(
        f"\nTotal recommendations generated: "
        f"{len(recommendations)}"
    )

    # -------------------------------------------------
    # 12. LEARNING PATHS
    # -------------------------------------------------

    learning_paths = generate_learning_paths(
        recommendations
    )

    learning_paths_df = pd.DataFrame(
        learning_paths
    )

    save_csv(
        learning_paths_df,
        "data/output/learning_paths.csv",
    )

    print("\nLearning Paths Preview:\n")

    for path in learning_paths[:10]:
        print(path)

    print(
        f"\nTotal learning-path records generated: "
        f"{len(learning_paths)}"
    )
        # -------------------------------------------------
    # JSON EXPORTS
    # -------------------------------------------------

    json_exports = [
        (
            learners,
            "data/output/learners.json",
        ),
        (
            courses,
            "data/output/courses.json",
        ),
        (
            skills,
            "data/output/skills.json",
        ),
        (
            skill_prerequisites,
            "data/output/skill_prerequisites.json",
        ),
        (
            content_items,
            "data/output/content_items.json",
        ),
        (
            content_skill_mapping,
            "data/output/content_skill.json",
        ),
        (
            attempts,
            "data/output/attempts.json",
        ),
        (
            assessment_results,
            "data/output/assessment_results.json",
        ),
        (
            mastery_records,
            "data/output/mastery.json",
        ),
        (
            recommendations,
            "data/output/recommendations.json",
        ),
        (
            learning_paths,
            "data/output/learning_paths.json",
        ),
    ]

    for records, file_path in json_exports:
        save_json(
            records,
            file_path,
        )

    print(
        f"\nJSON datasets generated: "
        f"{len(json_exports)}"
    )
    # -------------------------------------------------
    # 13. CLEAN BASELINE VALIDATION
    # -------------------------------------------------

    validation_issues = run_validation(
        learners=learners,
        courses=courses,
        skills=skills,
        content_items=content_items,
        content_skill_mapping=content_skill_mapping,
        attempts=attempts,
        assessment_results=assessment_results,
        mastery_records=mastery_records,
        recommendations=recommendations,
        learning_paths=learning_paths,
        skill_prerequisites=skill_prerequisites,
    )

    export_validation_summary(
        validation_issues,
        "data/output/validation_summary.csv",
        "data/output/validation_summary.json",
    )

    print(
        "\nClean baseline validation issues: "
        f"{len(validation_issues)}"
    )
        # -------------------------------------------------
    # 14. METRICS
    # -------------------------------------------------

    metrics = calculate_metrics(
        learners=learners,
        assessment_results=assessment_results,
        recommendations=recommendations,
        validation_issues=validation_issues,
    )

    with open(
        "data/output/metrics.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            metrics,
            file,
            indent=2,
        )

    print("\nMetrics:\n")

    for metric_name, metric_value in metrics.items():
        print(
            f"{metric_name}: {metric_value}"
        )
    # -------------------------------------------------
    # 14. CONTROLLED ANOMALIES + GROUND TRUTH
    # -------------------------------------------------

    _, prerequisite_gt = (
        inject_prerequisite_violation(
            recommendations
        )
    )

    _, timestamp_gt = (
        inject_invalid_attempt_timestamp(
            attempts
        )
    )

    _, content_skill_gt = (
        inject_invalid_content_skill(
            content_skill_mapping
        )
    )

    _, mastery_gt = (
        inject_future_mastery_leakage(
            mastery_records
        )
    )

    _, learning_path_gt = (
        inject_learning_path_loop(
            learning_paths
        )
    )

    ground_truth_records = [
        prerequisite_gt,
        timestamp_gt,
        content_skill_gt,
        mastery_gt,
        learning_path_gt,
    ]

    export_ground_truth(
        ground_truth_records,
        "data/output/ground_truth.csv",
        "data/output/ground_truth.json",
    )

    print(
        "\nGround truth anomalies generated: "
        f"{len(ground_truth_records)}"
    )
        # -------------------------------------------------
    # REPRODUCIBILITY CHECKSUMS
    # -------------------------------------------------

    output_files = [
        "data/output/learners.csv",
        "data/output/courses.csv",
        "data/output/skills.csv",
        "data/output/skill_prerequisites.csv",
        "data/output/content_items.csv",
        "data/output/content_skill.csv",
        "data/output/attempts.csv",
        "data/output/assessment_results.csv",
        "data/output/mastery.csv",
        "data/output/recommendations.csv",
        "data/output/learning_paths.csv",
        "data/output/ground_truth.csv",
        "data/output/ground_truth.json",
        "data/output/validation_summary.csv",
        "data/output/validation_summary.json",
        "data/output/metrics.json",
    ]

    checksum_manifest = create_checksum_manifest(
        file_paths=output_files,
        output_path="data/output/checksums.json",
    )

    print(
        "\nChecksums generated: "
        f"{len(checksum_manifest)}"
    )
    # -------------------------------------------------
    # 15. GENERATION SUMMARY
    # -------------------------------------------------

    print("\n" + "=" * 60)
    print("Generation Summary")
    print("=" * 60)

    print(
        f"Learners: {len(learners)}"
    )

    print(
        f"Courses: {len(courses)}"
    )

    print(
        f"Skills: {len(skills)}"
    )

    print(
        f"Skill prerequisites: "
        f"{len(skill_prerequisites)}"
    )

    print(
        f"Content items: "
        f"{len(content_items)}"
    )

    print(
        f"Content-skill mappings: "
        f"{len(content_skill_mapping)}"
    )

    print(
        f"Attempts: {len(attempts)}"
    )

    print(
        f"Assessment results: "
        f"{len(assessment_results)}"
    )

    print(
        f"Mastery records: "
        f"{len(mastery_records)}"
    )

    print(
        f"Recommendations: "
        f"{len(recommendations)}"
    )

    print(
        f"Learning paths: "
        f"{len(learning_paths)}"
    )

    print(
        f"Clean validation issues: "
        f"{len(validation_issues)}"
    )

    print(
        f"Ground truth anomalies: "
        f"{len(ground_truth_records)}"
    )

    print("=" * 60)
    print(
        "Generation completed successfully."
    )
    print("=" * 60)


if __name__ == "__main__":
    main()