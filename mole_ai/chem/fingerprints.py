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
    mol : RDKit Mol
        Molecule object.
    radius : int
        Morgan fingerprint radius.
    n_bits : int
        Number of fingerprint bits.

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


def morgan_fingerprint(
    mol,
    radius=2,
    n_bits=2048,
):
    """
    Backward-compatible alias for Morgan fingerprint generation.
    """

    return generate_morgan_fingerprint(
        mol,
        radius=radius,
        n_bits=n_bits,
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


def rank_by_similarity(
    query_fp,
    fingerprints,
):
    """
    Rank fingerprints by Tanimoto similarity.
    """

    similarities = [
        calculate_tanimoto_similarity(
            query_fp,
            fingerprint,
        )
        for fingerprint in fingerprints
    ]

    return sorted(
        similarities,
        reverse=True,
    )
