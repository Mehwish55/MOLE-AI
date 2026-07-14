from mole_ai.chem.smiles import smiles_to_mol


def test_valid_smiles():

    mol = smiles_to_mol("CCO")

    assert mol is not None



def test_invalid_smiles():

    mol = smiles_to_mol("INVALID")

    assert mol is None
