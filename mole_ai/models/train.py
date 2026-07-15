"""
Model training utilities for MOLE-AI.
"""

import pandas as pd


def load_feature_dataset(file_path: str) -> pd.DataFrame:
    """
    Load the engineered feature dataset.

    Parameters
    ----------
    file_path : str
        Path to the feature CSV.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset.
    """
    return pd.read_csv(file_path)
