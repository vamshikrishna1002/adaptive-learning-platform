from src.id_generator import generate_id
import random


def generate_courses(count: int):
    categories = [
        "Programming",
        "Databases",
        "Machine Learning",
        "Deep learning",
        "Gen AI"
    ]

    courses = []

    for i in range(1, count + 1):
        courses.append(
            {
                "course_id": generate_id("CRS", i),
                "course_name": f"Course {i}",
                "course_category": random.choice(categories)
            }
        )

    return courses