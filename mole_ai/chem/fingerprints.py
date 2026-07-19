"""
Molecular fingerprint utilities for MOLE-AI.
"""

from rdkit.Chem import AllChem
from rdkit.DataStructs import TanimotoSimilarity


def generate_morgan_fingerprint(
    mol,
    radius=2,
    n_bits=2048,
):
    """
    Generate a Morgan fingerprint.

    Parameters
    ----------
    mol : rdkit.Chem.Mol
        RDKit molecule object.

    radius : int
        Fingerprint radius.

    n_bits : int
        Fingerprint length.

    Returns
    -------
    ExplicitBitVect
        Morgan fingerprint.
    """

    return AllChem.GetMorganFingerprintAsBitVect(
        mol,
        radius,
        nBits=n_bits,
    )


def calculate_tanimoto_similarity(
    fingerprint1,
    fingerprint2,
):
    """
    Calculate Tanimoto similarity between two fingerprints.
    """

    return TanimotoSimilarity(
        fingerprint1,
        fingerprint2,
    )
