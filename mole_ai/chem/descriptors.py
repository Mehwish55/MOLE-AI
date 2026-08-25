"""
Molecular descriptor utilities for MOLE-AI.
"""

from rdkit.Chem import Descriptors
from rdkit.Chem import Lipinski
from rdkit.Chem import rdMolDescriptors


def calculate_descriptors(mol):
    """
    Calculate molecular descriptors for an RDKit molecule.

    Parameters
    ----------
    mol : RDKit Mol
        RDKit molecule object.

    Returns
    -------
    dict
        Dictionary containing standardized molecular descriptors.
    """

    if mol is None:
        raise ValueError("Invalid molecule: mol cannot be None")

    descriptors = {
        "molecular_formula": rdMolDescriptors.CalcMolFormula(mol),

        "molecular_weight": round(
            Descriptors.MolWt(mol), 2
        ),

        "exact_molecular_weight": round(
            Descriptors.ExactMolWt(mol), 2
        ),

        "logp": round(
            Descriptors.MolLogP(mol), 2
        ),

        "tpsa": round(
            Descriptors.TPSA(mol), 2
        ),

        "heavy_atom_count": Descriptors.HeavyAtomCount(mol),

        "hbd": Lipinski.NumHDonors(mol),

        "hba": Lipinski.NumHAcceptors(mol),

        "rotatable_bonds": Lipinski.NumRotatableBonds(mol),

        "ring_count": rdMolDescriptors.CalcNumRings(mol),

        "aromatic_ring_count": rdMolDescriptors.CalcNumAromaticRings(mol),

        "fraction_csp3": round(
            rdMolDescriptors.CalcFractionCSP3(mol), 3
        ),

        "formal_charge": sum(
            atom.GetFormalCharge() for atom in mol.GetAtoms()
        ),
    }

    return descriptors


# Backward-compatible alias
get_molecular_properties = calculate_descriptors
