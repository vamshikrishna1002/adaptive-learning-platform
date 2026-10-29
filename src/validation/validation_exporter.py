import json

import pandas as pd


def export_validation_summary(
    validation_issues,
    csv_path,
    json_path,
):
    """
    Export validation issues to CSV and JSON.
    """

    dataframe = pd.DataFrame(
        validation_issues
    )

    if dataframe.empty:
        dataframe = pd.DataFrame(
            columns=[
                "entity_type",
                "entity_id",
                "issue_type",
            ]
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
            validation_issues,
            file,
            indent=2,
            default=str,
        )