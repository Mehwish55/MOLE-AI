"""
Dataset validation functions for MOLE-AI.
"""

import pandas as pd


def validate_columns(
    df: pd.DataFrame,
    required_columns: list[str] | None = None
) -> bool:
    """
    Validate required columns in a dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset.

    required_columns : list[str], optional
        Required column names.

    Returns
    -------
    bool
        True if validation passes.

    Raises
    ------
    ValueError
        If required columns are missing.
    """

    if required_columns is None:
        required_columns = ["smiles", "activity"]

    missing = set(required_columns) - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    return True
