from mole_ai.chem.smiles import validate_smiles


def test_app_smiles_validation():

    assert validate_smiles("CCO") is True


def test_app_invalid_smiles():

    assert validate_smiles("INVALID") is False
