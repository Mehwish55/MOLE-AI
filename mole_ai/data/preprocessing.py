"""
Data preprocessing utilities for MOLE-AI.

Functions in this module clean molecular datasets
before machine learning workflows.
"""

import pandas as pd


def remove_missing(
    df: pd.DataFrame,
    columns: list[str] | None = None
) -> pd.DataFrame:
    """
    Remove rows with missing values.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset.

    columns : list[str], optional
        Columns to check for missing values.

    Returns
    -------
    pandas.DataFrame
        Cleaned dataset.
    """

    if columns is None:
        columns = ["smiles", "activity"]

    return df.dropna(subset=columns).reset_index(drop=True)



def remove_duplicates(
    df: pd.DataFrame,
    column: str = "smiles"
) -> pd.DataFrame:
    """
    Remove duplicate molecules.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset.

    column : str
        Column containing molecular identifiers.

    Returns
    -------
    pandas.DataFrame
        Dataset without duplicates.
    """

    return (
        df
        .drop_duplicates(subset=[column])
        .reset_index(drop=True)
    )
