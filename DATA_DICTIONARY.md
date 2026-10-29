# Adaptive Learning Platform - Data Dictionary

## Purpose

This data dictionary documents the synthetic data model used by the Adaptive Learning Platform. For each generated field it records the expected type, whether the field is required, key/relationship behavior, allowed values or units, uniqueness expectations, and the primary validation rule.

The core workflow is:

```text
Learner -> Attempt -> Assessment Result -> Mastery -> Recommendation -> Learning Path
```

Skill prerequisites are modeled as a directed acyclic graph (DAG), and `ContentSkill` provides the bridge between learning content and skills.

## ID Conventions

| Entity | ID Pattern | Example |
|---|---|---|
| Learner | `LRN-######` | `LRN-000001` |
| Course | `CRS-######` | `CRS-000001` |
| Skill | `SKL-######` | `SKL-000001` |
| ContentItem | `CNT-######` | `CNT-000001` |
| Attempt | `ATT-<learner-id>-######` | `ATT-LRN-000001-000001` |
| LearningPath | `PATH-2026-######` | `PATH-2026-000001` |

IDs are deterministic, zero-padded, immutable after generation, and references must match the corresponding parent ID exactly.

---

## 1. Learner

**Purpose:** Stores learner master data.

**Primary key:** `learner_id`

| Field | Type | Required | Key / Unique | Allowed Values / Units | Description | Validation Rule |
|---|---|---:|---|---|---|---|
| `learner_id` | VARCHAR(20) / string | Yes | PK, unique | `LRN-######` | Unique learner identifier | Must be non-null, unique, and follow the deterministic ID convention |
| `learner_status` | VARCHAR(20) / string | Yes | No | `REGISTERED`, `ACTIVE`, `INACTIVE`, `SUSPENDED` | Current learner lifecycle status | Must belong to the allowed status enum |
| `registration_date` | DATE / date | Yes | No | Calendar date | Date the learner was registered | Must be a valid date |

**Relationships:** One Learner can have many Attempts, Mastery records, Recommendations, and LearningPath records.

---

## 2. Course

**Purpose:** Represents a learning program or course.

**Primary key:** `course_id`

| Field | Type | Required | Key / Unique | Allowed Values / Units | Description | Validation Rule |
|---|---|---:|---|---|---|---|
| `course_id` | VARCHAR(20) / string | Yes | PK, unique | `CRS-######` | Unique course identifier | Must be non-null, unique, and follow the ID convention |
| `course_name` | VARCHAR(255) / string | Yes | No | Text | Human-readable course name | Must be non-null |
| `course_category` | VARCHAR(100) / string | Yes | No | Generated category text | Course subject/category | Must be non-null |

**Relationships:** Course is master data. The current synthetic implementation does not require a direct FK from event records to Course.

---

## 3. Skill

**Purpose:** Represents a knowledge unit in the prerequisite graph.

**Primary key:** `skill_id`

| Field | Type | Required | Key / Unique | Allowed Values / Units | Description | Validation Rule |
|---|---|---:|---|---|---|---|
| `skill_id` | VARCHAR(20) / string | Yes | PK, unique | `SKL-######` | Unique skill identifier | Must be non-null, unique, and follow the ID convention |
| `skill_name` | VARCHAR(255) / string | Yes | No | Text | Skill/knowledge-unit name | Must be non-null |

**Relationships:** A Skill can be a parent or child in SkillPrerequisite, can map to many ContentItems through ContentSkill, can have many Mastery records, and can appear in Recommendations and LearningPaths.

---

## 4. SkillPrerequisite

**Purpose:** Stores directed parent-skill to child-skill relationships forming the skill DAG.

**Primary key:** (`parent_skill_id`, `child_skill_id`)

| Field | Type | Required | Key / Unique | Allowed Values / Units | Description | Validation Rule |
|---|---|---:|---|---|---|---|
| `parent_skill_id` | VARCHAR(20) / string | Yes | Composite PK, FK -> Skill | Valid `skill_id` | Prerequisite skill | Must exist in Skill; cannot equal `child_skill_id` |
| `child_skill_id` | VARCHAR(20) / string | Yes | Composite PK, FK -> Skill | Valid `skill_id` | Skill unlocked after prerequisite | Must exist in Skill; pair must be unique |

**Cardinality:** Skill to Skill is modeled as directed 1:N relationships via this bridge. The complete graph must remain acyclic.

---

## 5. ContentItem

**Purpose:** Represents a learning resource that can be recommended or attempted.

**Primary key:** `content_id`

| Field | Type | Required | Key / Unique | Allowed Values / Units | Description | Validation Rule |
|---|---|---:|---|---|---|---|
| `content_id` | VARCHAR(20) / string | Yes | PK, unique | `CNT-######` | Unique content identifier | Must be non-null, unique, and follow the ID convention |
| `content_title` | VARCHAR(255) / string | Yes | No | Text | Content/resource title | Must be non-null |
| `content_type` | VARCHAR(30) / string | Yes | No | `VIDEO`, `QUIZ`, `ARTICLE`, `LAB`, `PROJECT` | Learning-resource format | Must belong to the allowed content-type enum |
| `difficulty` | VARCHAR(30) / string | Yes | No | `BEGINNER`, `INTERMEDIATE`, `ADVANCED` | Content difficulty | Must belong to the allowed difficulty enum |

**Relationships:** A ContentItem can map to one or more Skills through ContentSkill and can be referenced by many Attempts and Recommendations.

---

## 6. ContentSkill

**Purpose:** Bridge table relating content to the skills it teaches.

**Primary key:** (`content_id`, `skill_id`)

| Field | Type | Required | Key / Unique | Allowed Values / Units | Description | Validation Rule |
|---|---|---:|---|---|---|---|
| `content_id` | VARCHAR(20) / string | Yes | Composite PK, FK -> ContentItem | Valid `content_id` | Mapped content | Must exist in ContentItem |
| `skill_id` | VARCHAR(20) / string | Yes | Composite PK, FK -> Skill | Valid `skill_id` | Skill taught by the content | Must exist in Skill |

**Cardinality:** N:M between ContentItem and Skill. Duplicate (`content_id`, `skill_id`) pairs are invalid.

---

## 7. Attempt

**Purpose:** Stores learner activity against learning content.

**Primary key:** `attempt_id`

| Field | Type | Required | Key / Unique | Allowed Values / Units | Description | Validation Rule |
|---|---|---:|---|---|---|---|
| `attempt_id` | VARCHAR(50) / string | Yes | PK, unique | `ATT-<learner-id>-######` | Unique attempt/event identifier | Must be unique and immutable |
| `learner_id` | VARCHAR(20) / string | Yes | FK -> Learner | Valid `learner_id` | Learner performing the attempt | Must exist in Learner |
| `content_id` | VARCHAR(20) / string | Yes | FK -> ContentItem | Valid `content_id` | Content being attempted | Must exist in ContentItem |
| `attempt_timestamp` | DATETIME / datetime | Yes | No | Timestamp | Time of learner attempt | Must be valid and respect intended event ordering |

**Cardinality:** One Learner has many Attempts; one ContentItem can have many Attempts.

**History rule:** Attempts are event records and should be retained rather than overwritten.

---

## 8. AssessmentResult

**Purpose:** Stores the outcome produced by an Attempt.

**Primary key:** `attempt_id`

| Field | Type | Required | Key / Unique | Allowed Values / Units | Description | Validation Rule |
|---|---|---:|---|---|---|---|
| `attempt_id` | VARCHAR(50) / string | Yes | PK, FK -> Attempt | Valid `attempt_id` | Attempt that produced the result | Must exist in Attempt; one result per attempt |
| `learner_id` | VARCHAR(20) / string | Yes | FK -> Learner | Valid `learner_id` | Learner lineage copied from Attempt | Must match a valid Learner and source Attempt |
| `content_id` | VARCHAR(20) / string | Yes | FK -> ContentItem | Valid `content_id` | Content lineage copied from Attempt | Must match a valid ContentItem and source Attempt |
| `score` | INT / integer | Yes | No | 0-100 points | Assessment score | Must be between 0 and 100 inclusive |
| `pass_flag` | BOOLEAN | Yes | No | `True` / `False` | Derived pass/fail status | Must reconcile with the score rule; current generator uses score >= 60 as pass |
| `attempt_timestamp` | DATETIME / datetime | Yes | No | Timestamp | Source Attempt timestamp | Must match the source Attempt timestamp |

**Derived-value rule:** `pass_flag` is calculated from `score`, not generated independently.

---

## 9. Mastery

**Purpose:** Stores normalized learner proficiency for a Skill as of a specific timestamp.

**MySQL primary key:** (`learner_id`, `skill_id`, `mastery_as_of_timestamp`)

| Field | Type | Required | Key / Unique | Allowed Values / Units | Description | Validation Rule |
|---|---|---:|---|---|---|---|
| `learner_id` | VARCHAR(20) / string | Yes | FK -> Learner | Valid `learner_id` | Learner whose mastery is measured | Must exist in Learner |
| `skill_id` | VARCHAR(20) / string | Yes | FK -> Skill | Valid `skill_id` | Skill being measured | Must exist in Skill |
| `mastery_score` | DECIMAL(6,4) / float | Yes | No | 0.0000-1.0000 | Normalized proficiency estimate | Must remain in [0,1] and be derived from past AssessmentResults |
| `mastery_as_of_timestamp` | DATETIME / datetime | Yes | Part of PK | Timestamp | Latest time included in the mastery calculation | Source evidence must not occur after this cutoff |

**Temporal rule:** Future Attempts/AssessmentResults must not influence a mastery value calculated for an earlier `mastery_as_of_timestamp`.

---

## 10. Recommendation

**Purpose:** Records the skill/content decision produced by the recommendation engine and its rationale.

**MySQL primary key:** `recommendation_id` (auto-generated database surrogate key)

| Field | Type | Required | Key / Unique | Allowed Values / Units | Description | Validation Rule |
|---|---|---:|---|---|---|---|
| `recommendation_id` | BIGINT | DB-generated | PK, unique | Positive integer | MySQL surrogate key | Auto-incremented by MySQL |
| `learner_id` | VARCHAR(20) / string | Yes | FK -> Learner | Valid `learner_id` | Learner receiving recommendation | Must exist in Learner |
| `previous_skill_id` | VARCHAR(20) / string | Optional | FK -> Skill | Valid `skill_id` or null | Skill before recommendation; null for cold start | If provided, must exist in Skill |
| `recommended_skill_id` | VARCHAR(20) / string | Yes | FK -> Skill | Valid `skill_id` | Skill selected for the learner | Must exist in Skill and comply with prerequisite rules |
| `recommended_content_id` | VARCHAR(20) / string | Optional | FK -> ContentItem | Valid `content_id` or null | Content selected for the recommended skill | If present, must map to `recommended_skill_id` through ContentSkill |
| `reason_code` | VARCHAR(50) / string | Yes | No | Current implementation: `PREREQ_MET`, `LOW_MASTERY_REVIEW`, `RETRY_FAILED_CONTENT`, `COLD_START_DEFAULT` | Explains the decision | Must be non-null and belong to the supported reason-code set |
| `target_difficulty` | VARCHAR(30) / string | Optional | No | `BEGINNER`, `INTERMEDIATE`, `ADVANCED` | Difficulty selected from learner mastery | Must belong to difficulty enum when present |
| `recommended_difficulty` | VARCHAR(30) / string | Optional | No | `BEGINNER`, `INTERMEDIATE`, `ADVANCED` | Difficulty of selected content | Must match ContentItem difficulty when present |
| `difficulty_rank` | INT / integer | Optional | No | 1-3 | Numeric difficulty rank | 1=BEGINNER, 2=INTERMEDIATE, 3=ADVANCED |
| `difficulty_match` | BOOLEAN | Optional | No | `True` / `False` | Whether selected content matches target difficulty | Must equal comparison of target and selected difficulties when both exist |

**Business rules:**

```text
Mastery < 0.60      -> target BEGINNER
Mastery 0.60-0.79   -> target INTERMEDIATE
Mastery >= 0.80     -> target ADVANCED / eligible graph advancement
```

Repeated failures may produce `RETRY_FAILED_CONTENT`; learners without history use `COLD_START_DEFAULT`.

---

## 11. LearningPath

**Purpose:** Records the learner's skill position/transition derived from Recommendation.

**Primary key:** `path_id`

| Field | Type | Required | Key / Unique | Allowed Values / Units | Description | Validation Rule |
|---|---|---:|---|---|---|---|
| `path_id` | VARCHAR(30) / string | Yes | PK, unique | `PATH-2026-######` | Unique learning-path record | Must be unique and follow ID convention |
| `learner_id` | VARCHAR(20) / string | Yes | FK -> Learner | Valid `learner_id` | Learner associated with path | Must exist in Learner |
| `current_skill_id` | VARCHAR(20) / string | Yes | FK -> Skill | Valid `skill_id` | Current/recommended skill | Must exist in Skill |
| `previous_skill_id` | VARCHAR(20) / string | Optional | FK -> Skill | Valid `skill_id` or null | Previous skill; null may represent cold start | If provided, must exist in Skill |

**Loop rule:** Same-skill transitions are valid for review/retry and terminal-skill behavior; an invalid loop is a no-progress transition when advancement was expected.

---

## 12. Ground Truth

**Purpose:** Stores labels for deliberately injected anomalies separately from clean generation inputs.

| Field | Type | Required | Key / Unique | Allowed Values / Units | Description | Validation Rule |
|---|---|---:|---|---|---|---|
| `anomaly_id` | string | Yes | Unique | `ANM-######` | Controlled anomaly identifier | Must be unique |
| `entity_type` | string | Yes | No | `RECOMMENDATION`, `ATTEMPT`, `CONTENT_SKILL`, `MASTERY`, `LEARNING_PATH` | Entity containing the injected anomaly | Must identify the affected dataset |
| `entity_id` | string | Yes | No | Entity-specific identifier | Record associated with the anomaly | Must identify the deliberately modified record |
| `issue_type` | string | Yes | No | See anomaly types below | Ground-truth anomaly label | Must belong to documented anomaly set |
| `description` | string | Yes | No | Text | Human-readable anomaly explanation | Must be non-empty |

Controlled issue types:

```text
PREREQUISITE_VIOLATION
INVALID_ATTEMPT_TIMESTAMP_ORDER
INVALID_CONTENT_SKILL_REFERENCE
FUTURE_MASTERY_LEAKAGE
LEARNING_PATH_LOOP
```

Some anomaly records include additional before/after fields such as original/anomalous skill IDs or timestamps for traceability.

---

## 13. Validation Summary

**Purpose:** Stores issues detected by the validation framework.

| Field | Type | Required | Description |
|---|---|---:|---|
| `entity_type` | string | Yes | Dataset/entity where the issue was detected |
| `entity_id` | string | Context-dependent | Identifier of the affected record when available |
| `issue_type` | string | Yes | Validation failure category |
| Additional fields | mixed | Context-dependent | Evidence such as field name, invalid value, previous timestamp, or skill IDs |

A clean baseline is expected to produce zero issue rows. Controlled anomalies are recorded separately in Ground Truth.

---

## 14. Metrics Output

**Purpose:** Provides measurable outputs for assessment and recommendation behavior.

| Field | Type | Units | Description |
|---|---|---|---|
| `total_learners` | integer | records | Number of learners evaluated |
| `total_assessments` | integer | records | Number of assessment results evaluated |
| `total_recommendations` | integer | records | Number of recommendations generated |
| `recommendation_coverage` | float | proportion 0-1 | Proportion of learners receiving at least one recommendation |
| `pass_rate` | float | proportion 0-1 | Proportion of assessments with `pass_flag=True` |
| `difficulty_match_rate` | float | proportion 0-1 | Proportion of recommendations whose content difficulty matches target difficulty |
| `cold_start_rate` | float | proportion 0-1 | Proportion of recommendations using `COLD_START_DEFAULT` |
| `prerequisite_violation_rate` | float | proportion 0-1 | Detected prerequisite violations divided by recommendations |

---

## Cardinality Summary

| Relationship | Cardinality | Notes |
|---|---|---|
| Learner -> Attempt | 1:N | A learner can generate many attempts |
| ContentItem -> Attempt | 1:N | Content can be attempted many times |
| Attempt -> AssessmentResult | 1:1 | Each generated attempt has one assessment result |
| Skill -> SkillPrerequisite | 1:N | A skill may participate in prerequisite edges |
| ContentItem <-> Skill | N:M | Implemented through ContentSkill |
| Learner -> Mastery | 1:N | Learner may have mastery for multiple skills/as-of times |
| Skill -> Mastery | 1:N | A skill may have mastery records for many learners |
| Learner -> Recommendation | 1:N | Learner may receive recommendation records |
| Skill -> Recommendation | 1:N | Skill may be recommended to many learners |
| Learner -> LearningPath | 1:N | Learner may have progression/path history |

---

## Lifecycle and Temporal Rules

1. Master/reference data is generated before dependent event data.
2. Child records must use valid parent IDs in the clean baseline.
3. Attempts and AssessmentResults are historical events and are retained rather than overwritten.
4. Assessment-derived values are calculated from their source records.
5. Mastery uses only source evidence available on or before `mastery_as_of_timestamp`.
6. Recommendations preserve rationale through `reason_code` and skill/content references.
7. LearningPath preserves skill-transition traceability through previous/current skill IDs.
8. Ground Truth remains separate from clean model inputs.

---

## Validation Coverage

The implementation validates:

- primary-key uniqueness,
- foreign-key integrity,
- duplicate bridge records,
- allowed enums,
- assessment score range,
- pass-flag reconciliation,
- mastery range,
- Attempt timestamp ordering,
- Mastery temporal leakage,
- prerequisite compliance,
- recommendation ContentSkill consistency,
- reason codes,
- learning-path loops,
- skill DAG integrity.

The MySQL schema in `sql/schema.sql` is the authoritative source for database column types, keys, CHECK constraints, and indexes.
