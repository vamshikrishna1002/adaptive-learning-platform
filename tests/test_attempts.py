from src.events.attempt_generator import generate_attempts
from config.settings import STARTER_SCALE

def test_attempt_count():
    attempts = generate_attempts()

    assert len(attempts) == 5
    
def test_attempt_ids_are_unique():
    attempts = generate_attempts()

    attempt_ids = [
        attempt["attempt_id"]
        for attempt in attempts
    ]

    assert len(attempt_ids) == len(set(attempt_ids))


def test_attempt_timestamps_are_in_order():
    attempts = generate_attempts()

    timestamps = [
        attempt["attempt_timestamp"]
        for attempt in attempts
    ]

    assert timestamps == sorted(timestamps)
    
from src.generators.learner_generator import generate_learners
from src.generators.content_generator import generate_content_items


def test_attempt_foreign_keys_are_valid():
    learners = generate_learners(100)
    content_items = generate_content_items(5)
    attempts = generate_attempts()

    learner_ids = {
        learner["learner_id"]
        for learner in learners
    }

    content_ids = {
        content["content_id"]
        for content in content_items
    }

    for attempt in attempts:
        assert attempt["learner_id"] in learner_ids
        assert attempt["content_id"] in content_ids
        
def test_starter_scale_attempt_count():
    attempts = generate_attempts(
        count=STARTER_SCALE["attempts"],
        content_count=STARTER_SCALE["content_items"]
    )

    assert len(attempts) == STARTER_SCALE["attempts"]


def test_attempts_are_distributed_across_learners():
    attempts = generate_attempts(
        count=500,
        content_count=5,
        learner_count=100
    )

    learner_ids = {
        attempt["learner_id"]
        for attempt in attempts
    }

    assert len(learner_ids) == 100

def test_cold_start_learners_have_no_attempts():
    total_learners = 100
    active_learner_count = 90

    attempts = generate_attempts(
        count=500,
        content_count=5,
        learner_count=active_learner_count
    )

    learners_with_attempts = {
        attempt["learner_id"]
        for attempt in attempts
    }

    cold_start_learners = {
        f"LRN-{learner_number:06d}"
        for learner_number in range(91, total_learners + 1)
    }

    assert learners_with_attempts.isdisjoint(
        cold_start_learners
    )

    assert len(cold_start_learners) == 10
def test_full_scale_configuration_smoke_test():
    learner_count = 10_000
    skill_count = 500
    content_count = 2_000

    active_learner_count = int(
        learner_count * 0.90
    )

    attempts = generate_attempts(
        count=1_000,
        content_count=content_count,
        learner_count=active_learner_count,
    )

    assert len(attempts) == 1_000

    learner_ids = {
        attempt["learner_id"]
        for attempt in attempts
    }

    content_ids = {
        attempt["content_id"]
        for attempt in attempts
    }

    assert len(learner_ids) == 1_000
    assert len(content_ids) == 1_000

    assert all(
        1 <= int(
            attempt["learner_id"].split("-")[-1]
        ) <= active_learner_count
        for attempt in attempts
    )

    assert all(
        1 <= int(
            attempt["content_id"].split("-")[-1]
        ) <= content_count
        for attempt in attempts
    )