import pandas as pd

from mole_ai.models.optimization import rank_candidates


def test_rank_candidates():

    candidates = pd.DataFrame(
        {
            "smiles": [
                "CCO",
                "CCN",
                "CCC",
            ],
            "predicted_pIC50": [
                7.5,
                8.2,
                6.8,
            ],
            "admet_prediction": [
                0.9,
                0.7,
                0.8,
            ],
        }
    )

    ranked = rank_candidates(candidates)

    assert len(ranked) == 3

    assert "optimization_score" in ranked.columns

    assert (
        ranked.iloc[0]["optimization_score"]
        >= ranked.iloc[1]["optimization_score"]
    )


def test_custom_weights():

    candidates = pd.DataFrame(
        {
            "smiles": ["CCO"],
            "predicted_pIC50": [8.0],
            "admet_prediction": [0.5],
        }
    )

    ranked = rank_candidates(
        candidates,
        activity_weight=0.5,
        admet_weight=0.5,
    )

    expected = (0.5 * 8.0) + (0.5 * 0.5)

    assert ranked.iloc[0]["optimization_score"] == expected
