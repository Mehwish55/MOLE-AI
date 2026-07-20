"""
Dataset metadata utilities for MOLE-AI.
"""

import json
from datetime import datetime

import pandas as pd


def generate_dataset_metadata(df: pd.DataFrame):
    """
    Generate dataset metadata.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset.

    Returns
    -------
    dict
        Dataset metadata.
    """

    metadata = {
        "created": str(datetime.now()),
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "columns": list(df.columns),
    }

    return metadata


def save_metadata(metadata: dict, output_path: str):
    """
    Save dataset metadata as JSON.
    """

    with open(output_path, "w") as file:
        json.dump(
            metadata,
            file,
            indent=4,
        )
