# Adaptive Learning Platform

## Overview

The Adaptive Learning Platform is a synthetic data generation and rules-based recommendation system designed to model learner activity, assessment performance, skill mastery, prerequisite relationships, and personalized learning recommendations.

The project demonstrates practical data engineering concepts including:

- Synthetic data generation
- Relational data modeling
- Event-driven learner activity modeling
- Directed Acyclic Graph (DAG) modeling
- Rules-based recommendation systems
- Data quality validation
- Temporal data integrity
- MySQL integration
- Controlled anomaly injection
- Ground-truth generation
- Metrics and evaluation
- Reproducibility using fixed random seeds and SHA-256 checksums

---

## Business Flow

The core learning workflow is:

Learner
→ Attempt
→ Assessment Result
→ Mastery
→ Skill Prerequisite Check
→ Recommendation
→ Recommended Content
→ Learning Path

A learner interacts with learning content through Attempts.

Each Attempt produces an Assessment Result.

Assessment Results are used to calculate learner mastery for skills.

The recommendation engine then evaluates mastery and the prerequisite graph to determine whether the learner should:

- review the current skill,
- retry previously failed content,
- advance to the next eligible skill, or
- receive a cold-start recommendation.

---

## Technology Stack

- Python 3
- Pandas
- NumPy
- pytest
- MySQL 8
- MySQL Workbench
- CSV
- JSON
- SQL
- SHA-256

---

## Project Structure

```text
adaptive-learning-platform/
│
├── config/
│   └── settings.py
│
├── data/
│   └── output/
│       ├── learners.csv
│       ├── courses.csv
│       ├── skills.csv
│       ├── skill_prerequisites.csv
│       ├── content_items.csv
│       ├── content_skill.csv
│       ├── attempts.csv
│       ├── assessment_results.csv
│       ├── mastery.csv
│       ├── recommendations.csv
│       ├── learning_paths.csv
│       ├── ground_truth.csv
│       ├── ground_truth.json
│       ├── validation_summary.csv
│       ├── validation_summary.json
│       ├── metrics.json
│       └── checksums.json
│
├── sql/
│   ├── schema.sql
│   ├── load_data.sql
│   └── validate_data.sql
│
├── src/
│   ├── anomalies/
│   ├── events/
│   ├── generators/
│   ├── metrics/
│   ├── reproducibility/
│   ├── validation/
│   ├── exporters.py
│   └── exporters_json.py
│
├── tests/
│
├── main.py
├── pytest.ini
├── requirements.txt
└── README.md