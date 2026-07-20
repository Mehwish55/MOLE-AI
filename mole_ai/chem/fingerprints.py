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


def rank_by_similarity(query_fp, fingerprints):
    """
    Rank fingerprints by Tanimoto similarity.

    Parameters
    ----------
    query_fp :
        Query molecular fingerprint.

    fingerprints : list
        Candidate fingerprints.

    Returns
    -------
    list
        Similarity scores sorted highest to lowest.
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


def morgan_fingerprint(
    mol,
    radius=2,
    n_bits=2048,
):
    """
    Compatibility wrapper for Morgan fingerprint generation.

    Parameters
    ----------
    mol :
        RDKit molecule object.

    radius :
        Morgan fingerprint radius.

    n_bits :
        Fingerprint size.

    Returns
    -------
    RDKit fingerprint
    """

    return generate_morgan_fingerprint(
        mol,
        radius,
        n_bits,
    )
