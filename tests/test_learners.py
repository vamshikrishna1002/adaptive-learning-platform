from src.generators.learner_generator import generate_learners


def test_learner_count():
    learners = generate_learners(100)

    assert len(learners) == 100
    
def test_learner_ids_are_unique():
    learners = generate_learners(100)

    learner_ids = [learner["learner_id"] for learner in learners]

    assert len(learner_ids) == len(set(learner_ids))