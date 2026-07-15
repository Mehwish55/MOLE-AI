"""
Model training utilities for MOLE-AI.
"""

import pandas as pd


def load_feature_dataset(file_path: str) -> pd.DataFrame:

def prepare_training_data(df: pd.DataFrame):
    """
    Split dataset into features (X) and target (y).

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    tuple
        X, y
    """

    X = df.drop(columns=["activity"])

    if "smiles" in X.columns:
        X = X.drop(columns=["smiles"])

    y = df["activity"]

    return X, y


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
