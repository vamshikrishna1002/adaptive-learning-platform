import json
import os

from src.reproducibility.checksum import (
    calculate_sha256,
)


def create_checksum_manifest(
    file_paths,
    output_path,
):
    """
    Create a SHA-256 checksum manifest
    for generated output files.
    """

    manifest = {}

    for file_path in file_paths:
        if not os.path.exists(file_path):
            continue

        file_name = os.path.basename(
            file_path
        )

        manifest[file_name] = {
            "sha256": calculate_sha256(
                file_path
            ),
            "size_bytes": os.path.getsize(
                file_path
            ),
        }

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            manifest,
            file,
            indent=2,
        )

    return manifest