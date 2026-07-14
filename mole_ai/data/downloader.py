"""
Data loading utilities for MOLE-AI.

This module provides functions to load molecular datasets
into pandas DataFrames.
"""

from pathlib import Path

import pandas as pd


def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load a CSV dataset.

    Parameters
    ----------
    file_path : str
        Path to the CSV file.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    return pd.read_csv(path)
