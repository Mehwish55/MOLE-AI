"""
Molecular descriptor calculation utilities.
"""

from rdkit.Chem import Crippen
from rdkit.Chem import Descriptors
from rdkit.Chem import Lipinski
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import rdmolops


def calculate_descriptors(mol):
    """
    Calculate molecular descriptors.

    Parameters
    ----------
    mol : rdkit.Chem.Mol
        RDKit molecule object.

    Returns
    -------
    dict
        Molecular descriptor values.
    """

    return {
        "molecular_weight": Descriptors.MolWt(mol),
        "logp": Crippen.MolLogP(mol),
        "hbd": Lipinski.NumHDonors(mol),
        "hba": Lipinski.NumHAcceptors(mol),
        "rotatable_bonds": Lipinski.NumRotatableBonds(mol),
        "tpsa": rdMolDescriptors.CalcTPSA(mol),
        "heavy_atom_count": mol.GetNumHeavyAtoms(),
        "aromatic_ring_count": rdMolDescriptors.CalcNumAromaticRings(mol),
        "fraction_csp3": rdMolDescriptors.CalcFractionCSP3(mol),
        "formal_charge": rdmolops.GetFormalCharge(mol),
             }
