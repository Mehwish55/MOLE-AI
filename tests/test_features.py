import pandas as pd

from mole_ai.features.builder import build_feature_matrix


def test_feature_matrix():

    df = pd.DataFrame(
        {
            "smiles": ["CCO"],
            "activity": [1]
        }
    )

    result = build_feature_matrix(df)

    assert len(result) == 1
    assert "molecular_weight" in result.columns
    assert "activity" in result.columns
