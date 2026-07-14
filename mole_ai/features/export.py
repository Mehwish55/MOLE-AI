"""
Feature matrix export utilities.
"""

import os
import pandas as pd


def save_features(
    df: pd.DataFrame,
    output_path: str
):
    """
    Save feature matrix as CSV.

    Parameters
    ----------
    df : pandas.DataFrame
        Generated feature matrix

    output_path : str
        Destination CSV path
    """

    directory = os.path.dirname(output_path)

    if directory:
        os.makedirs(
            directory,
            exist_ok=True
        )

    df.to_csv(
        output_path,
        index=False
    )
