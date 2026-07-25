"""
Molecular descriptor generation for QSAR modeling.
"""

from rdkit.Chem import Descriptors
from rdkit.Chem import Lipinski


def calculate_descriptors(mol):

    descriptors = {

        "Molecular Weight":
            Descriptors.MolWt(mol),

        "LogP":
            Descriptors.MolLogP(mol),

        "TPSA":
            Descriptors.TPSA(mol),

        "HBD":
            Lipinski.NumHDonors(mol),

        "HBA":
            Lipinski.NumHAcceptors(mol),

        "Rotatable Bonds":
            Lipinski.NumRotatableBonds(mol),

    }

    return descriptors
