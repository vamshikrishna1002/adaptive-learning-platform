import json
import pandas as pd


def export_ground_truth(
    ground_truth_records,
    csv_path,
    json_path,
):
    """
    Export anomaly ground truth to CSV and JSON.
    """

    valid_records = [
        record
        for record in ground_truth_records
        if record is not None
    ]

    dataframe = pd.DataFrame(
        valid_records
    )

    dataframe.to_csv(
        csv_path,
        index=False,
    )

    with open(
        json_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            valid_records,
            file,
            indent=2,
            default=str,
        )