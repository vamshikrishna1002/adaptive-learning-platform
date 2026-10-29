from src.id_generator import generate_id
from datetime import date
import random
STATUSES = [
    "REGISTERED",
    "ACTIVE",
    "INACTIVE",
    "SUSPENDED"
]

def generate_learners(count: int):
    learners = []

    for i in range(1, count + 1):
        learners.append(
    {
        "learner_id": generate_id("LRN", i),
        "learner_status": random.choice(STATUSES),
        "registration_date": date(2026, 1, 1)
    }
)


    return learners