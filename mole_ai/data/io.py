"""
Input/Output utilities for MOLE-AI.
"""

from pathlib import Path
import pandas as pd


def save_dataset(df: pd.DataFrame, output_path: str) -> None:
    """
    Save a cleaned dataset as a CSV file.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset to save.

    output_path : str
        Destination file path.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(path, index=False)
