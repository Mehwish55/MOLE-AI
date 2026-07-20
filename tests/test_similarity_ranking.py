from rdkit import Chem

from mole_ai.chem.fingerprints import (
    generate_morgan_fingerprint,
    rank_by_similarity,
)


def test_rank_by_similarity():

    query = Chem.MolFromSmiles("CCO")

    molecule1 = Chem.MolFromSmiles("CCCO")
    molecule2 = Chem.MolFromSmiles("c1ccccc1")
    molecule3 = Chem.MolFromSmiles("CCN")

    query_fp = generate_morgan_fingerprint(query)

    fingerprints = [
        generate_morgan_fingerprint(molecule1),
        generate_morgan_fingerprint(molecule2),
        generate_morgan_fingerprint(molecule3),
    ]

    rankings = rank_by_similarity(
        query_fp,
        fingerprints,
    )

    assert len(rankings) == 3

    assert rankings[0] >= rankings[1]
    assert rankings[1] >= rankings[2]

    for score in rankings:
        assert 0.0 <= score <= 1.0
