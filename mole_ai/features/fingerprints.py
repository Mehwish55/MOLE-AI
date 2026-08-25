"""
Fingerprint generation for machine-learning features.
"""

from mole_ai.chem.fingerprints import generate_morgan_fingerprint


def generate_fingerprint(
    mol,
    radius=2,
    n_bits=2048,
):
    """
    Generate a Morgan fingerprint for ML features.
    """

    return generate_morgan_fingerprint(
        mol,
        radius=radius,
        n_bits=n_bits,
    )
