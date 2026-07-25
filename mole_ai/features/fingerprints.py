"""
Fingerprint generation for QSAR models.
"""

from rdkit.Chem import AllChem


def generate_fingerprint(mol):

    fingerprint = AllChem.GetMorganFingerprintAsBitVect(
        mol,
        radius=2,
        nBits=2048
    )

    return fingerprint
