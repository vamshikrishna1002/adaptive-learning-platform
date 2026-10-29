from datetime import datetime, timedelta


def generate_attempts(
    count=5,
    content_count=5,
    learner_count=1
):
    """
    Generate synthetic learner attempts.

    Parameters
    ----------
    count : int
        Total number of attempts to generate.

    content_count : int
        Number of valid content items available.

    learner_count : int
        Number of valid learners available.

    Returns
    -------
    list[dict]
        Generated attempt records.
    """

    attempts = []

    base_time = datetime(
        2026,
        1,
        15,
        10,
        0,
        0
    )

    for attempt_number in range(1, count + 1):

        # Cycle through available learners.
        learner_number = (
            (attempt_number - 1) % learner_count
        ) + 1

        learner_id = f"LRN-{learner_number:06d}"

        # Cycle through available content items.
        # This also creates repeated attempts.
        content_number = (
            (attempt_number - 1) % content_count
        ) + 1

        content_id = f"CNT-{content_number:06d}"

        attempt_id = (
            f"ATT-{learner_id}-"
            f"{attempt_number:06d}"
        )

        attempt_timestamp = (
            base_time
            + timedelta(days=attempt_number - 1)
        )

        attempts.append(
            {
                "attempt_id": attempt_id,
                "learner_id": learner_id,
                "content_id": content_id,
                "attempt_timestamp": attempt_timestamp,
            }
        )

    return attempts