import json


def save_json(
    records,
    file_path,
):
    """
    Save generated records as formatted JSON.
    """

    with open(
        file_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            records,
            file,
            indent=2,
            default=str,
        )

    print(
        f"JSON saved: {file_path}"
    )