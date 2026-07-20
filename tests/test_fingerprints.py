from rdkit import Chem

from mole_ai.chem.fingerprints import (
    calculate_tanimoto_similarity,
    generate_morgan_fingerprint,
)


def test_generate_morgan_fingerprint():
    mol = Chem.MolFromSmiles("CCO")

    fingerprint = generate_morgan_fingerprint(mol)

    assert fingerprint is not None


def test_calculate_tanimoto_similarity():
    mol1 = Chem.MolFromSmiles("CCO")
    mol2 = Chem.MolFromSmiles("CCCO")

    fp1 = generate_morgan_fingerprint(mol1)
    fp2 = generate_morgan_fingerprint(mol2)

    similarity = calculate_tanimoto_similarity(fp1, fp2)

    assert 0.0 <= similarity <= 1.0
