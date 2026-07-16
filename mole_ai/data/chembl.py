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


import numpy as np


def ic50_to_pic50(ic50_nm):
    """
    Convert IC50 values from nM to pIC50.

    Parameters
    ----------
    ic50_nm : float
        IC50 value in nanomolar.

    Returns
    -------
    float
        pIC50 value.
    """

    ic50_molar = ic50_nm * 1e-9

    return -np.log10(ic50_molar)


def prepare_chembl_dataset(df):
    """
    Prepare ChEMBL data for QSAR modeling.

    Converts IC50 values to pIC50 and keeps
    required columns.
    """

    df = filter_activity_data(df)

    df["pIC50"] = df["IC50"].apply(ic50_to_pic50)

    return df[
        [
            "smiles",
            "pIC50",
        ]
    ]
