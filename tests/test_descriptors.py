from rdkit import Chem

from mole_ai.chem.descriptors import calculate_descriptors


def test_advanced_descriptors():

    mol = Chem.MolFromSmiles("CCOc1ccccc1")

    descriptors = calculate_descriptors(mol)

    expected_keys = [
        "molecular_weight",
        "logp",
        "hbd",
        "hba",
        "rotatable_bonds",
        "tpsa",
        "heavy_atom_count",
        "aromatic_ring_count",
        "fraction_csp3",
        "formal_charge",
    ]

    for key in expected_keys:
        assert key in descriptors

    assert descriptors["molecular_weight"] > 0
    assert descriptors["heavy_atom_count"] > 0
    assert descriptors["tpsa"] >= 0
