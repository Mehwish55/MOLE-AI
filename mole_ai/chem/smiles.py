"""
SMILES processing utilities for MOLE-AI.
"""

from rdkit import Chem


def smiles_to_mol(smiles: str):
    """
    Convert SMILES string to RDKit molecule.

    Parameters
    ----------
    smiles : str
        Molecular SMILES representation.

    Returns
    -------
    rdkit.Chem.Mol or None
        RDKit molecule object.
    """

    return Chem.MolFromSmiles(smiles)


def validate_smiles(smiles: str):
    """
    Validate a SMILES string.

    Parameters
    ----------
    smiles : str
        Molecular SMILES representation.

    Returns
    -------
    bool
        True if valid molecule.
    """

    molecule = smiles_to_mol(smiles)

    return molecule is not None
