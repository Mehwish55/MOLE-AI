"""
Molecular generation utilities for MOLE-AI.
"""

from rdkit import Chem


def validate_smiles(smiles):
    """
    Validate generated SMILES string.

    Parameters
    ----------
    smiles : str
        Molecular SMILES.

    Returns
    -------
    bool
        True if valid molecule.
    """

    molecule = Chem.MolFromSmiles(smiles)

    return molecule is not None


def generate_candidate_smiles(seed_smiles):
    """
    Generate molecular candidate from seed.

    This is a simple foundation for future
    generative models.

    Parameters
    ----------
    seed_smiles : str
        Starting molecule.

    Returns
    -------
    str
        Generated candidate SMILES.
    """

    molecule = Chem.MolFromSmiles(seed_smiles)

    if molecule is None:
        raise ValueError(
            "Invalid SMILES input"
        )

    return Chem.MolToSmiles(
        molecule
    )
