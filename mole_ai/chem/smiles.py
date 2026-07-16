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
