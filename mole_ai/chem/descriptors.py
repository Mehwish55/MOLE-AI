"""
Molecular descriptor utilities for MOLE-AI.
"""

from rdkit.Chem import Descriptors
from rdkit.Chem import Lipinski
from rdkit.Chem import rdMolDescriptors


def get_molecular_properties(mol):
    """
    Calculate molecular descriptors.

    Parameters
    ----------
    mol : RDKit Mol

    Returns
    -------
    dict
        Dictionary containing molecular properties.
    """

    properties = {

        "Formula":
        rdMolDescriptors.CalcMolFormula(mol),

        "Molecular Weight":
        round(
            Descriptors.MolWt(mol),
            2,
        ),

        "Exact Molecular Weight":
        round(
            Descriptors.ExactMolWt(mol),
            2,
        ),

        "LogP":
        round(
            Descriptors.MolLogP(mol),
            2,
        ),

        "TPSA":
        round(
            Descriptors.TPSA(mol),
            2,
        ),

        "Heavy Atoms":
        Descriptors.HeavyAtomCount(mol),

        "Hydrogen Bond Donors":
        Lipinski.NumHDonors(mol),

        "Hydrogen Bond Acceptors":
        Lipinski.NumHAcceptors(mol),

        "Rotatable Bonds":
        Lipinski.NumRotatableBonds(mol),

        "Ring Count":
        rdMolDescriptors.CalcNumRings(mol),

        "Aromatic Rings":
        rdMolDescriptors.CalcNumAromaticRings(mol),
    }

    return properties
