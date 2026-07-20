from mole_ai.chem.smiles import smiles_to_mol
from mole_ai.chem.descriptors import calculate_descriptors


def test_valid_smiles():

    mol = smiles_to_mol("CCO")

    assert mol is not None



def test_invalid_smiles():

    mol = smiles_to_mol("INVALID")

    assert mol is None



def test_descriptor_calculation():

    mol = smiles_to_mol("CCO")

    descriptors = calculate_descriptors(mol)

    assert "molecular_weight" in descriptors
    assert "logp" in descriptors
    assert descriptors["hbd"] == 1
