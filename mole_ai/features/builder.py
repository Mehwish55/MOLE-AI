"""
Feature engineering pipeline for MOLE-AI.

This module combines molecular descriptors and fingerprints
to create machine learning-ready feature matrices.
"""

import pandas as pd

from mole_ai.chem.smiles import smiles_to_mol
from mole_ai.chem.descriptors import calculate_descriptors
from mole_ai.chem.fingerprints import morgan_fingerprint


def fingerprint_to_array(fp):
    """
    Convert RDKit fingerprint to a list of bits.

    Parameters
    ----------
    fp : RDKit fingerprint

    Returns
    -------
    list
        Fingerprint bit values.
    """

    return list(fp)


def build_feature_matrix(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Convert molecular dataset into AI-ready features.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing SMILES column.

    Returns
    -------
    pandas.DataFrame
        Feature matrix.
    """

    features = []

    for _, row in df.iterrows():

        smiles = row["smiles"]

        mol = smiles_to_mol(smiles)

        if mol is None:
            continue

        descriptors = calculate_descriptors(mol)

        fingerprint = morgan_fingerprint(mol)

        fp_array = fingerprint_to_array(fingerprint)

        feature_row = {
            "smiles": smiles,
            **descriptors,
        }

        for i, value in enumerate(fp_array):
            feature_row[f"fp_{i}"] = value

        if "activity" in row:
            feature_row["activity"] = row["activity"]

        features.append(feature_row)

    return pd.DataFrame(features)
