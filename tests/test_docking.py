import pandas as pd

from mole_ai.models.docking import (
    create_docking_results,
    rank_docking_results,
)


def test_create_docking_results():

    smiles = [
        "CCO",
        "CCN",
        "CCC",
    ]

    affinity = [
        -7.5,
        -9.2,
        -8.1,
    ]

    results = create_docking_results(
        smiles,
        affinity,
    )

    assert isinstance(
        results,
        pd.DataFrame,
    )

    assert len(results) == 3

    assert "binding_affinity" in results.columns


def test_rank_docking_results():

    results = pd.DataFrame(
        {
            "smiles": [
                "CCO",
                "CCN",
                "CCC",
            ],
            "binding_affinity": [
                -7.5,
                -9.2,
                -8.1,
            ],
        }
    )

    ranked = rank_docking_results(
        results,
    )

    assert ranked.iloc[0]["binding_affinity"] == -9.2

    assert ranked.iloc[1]["binding_affinity"] == -8.1

    assert ranked.iloc[2]["binding_affinity"] == -7.5
