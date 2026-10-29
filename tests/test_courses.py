from src.generators.course_generator import generate_courses


def test_course_count():
    courses = generate_courses(5)

    assert len(courses) == 5
    
def test_course_ids_are_unique():
    courses = generate_courses(100)

    course_ids = [course["course_id"] for course in courses]

    assert len(course_ids) == len(set(course_ids))