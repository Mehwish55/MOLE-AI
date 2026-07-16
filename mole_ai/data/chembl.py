"""
ChEMBL data utilities for MOLE-AI.
"""

import pandas as pd


def load_chembl_csv(file_path):
    """
    Load ChEMBL bioactivity CSV data.
    """

    return pd.read_csv(file_path)


def filter_activity_data(df):
    """
    Keep only valid IC50 measurements.
    """

    required_columns = [
        "smiles",
        "IC50",
    ]

    df = df.dropna(
        subset=required_columns
    )

    return df
