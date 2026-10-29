from src.id_generator import generate_id
import random


def generate_content_items(count: int):

    content_types = [
        "VIDEO",
        "QUIZ",
        "ARTICLE",
        "LAB",
        "PROJECT"
    ]
    difficulty_levels = [
    "BEGINNER",
    "INTERMEDIATE",
    "ADVANCED"
    ]
    content_items = []

    for i in range(1, count + 1):
        content_items.append(
            {
                "content_id": generate_id("CNT", i),
                "content_title": f"Content {i}",
                "content_type": random.choice(content_types),
                "difficulty": random.choice(difficulty_levels)
            }
        )

    return content_items