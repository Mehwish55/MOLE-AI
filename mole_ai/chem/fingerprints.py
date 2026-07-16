"""
Molecular fingerprint generation utilities.
"""

from rdkit.Chem import rdFingerprintGenerator


def morgan_fingerprint(
    mol,
    radius: int = 2,
    n_bits: int = 2048
):
    """
    Generate Morgan fingerprint.

    Parameters
    ----------
    mol:
        RDKit molecule object

    radius:
        Morgan fingerprint radius

    n_bits:
        Fingerprint size

    Returns
    -------
    RDKit fingerprint
    """

    generator = rdFingerprintGenerator.GetMorganGenerator(
        radius=radius,
        fpSize=n_bits
    )

    return generator.GetFingerprint(mol)
