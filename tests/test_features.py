import pandas as pd

from mole_ai.features.builder import build_feature_matrix
from mole_ai.features.export import save_features


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



def test_feature_export(tmp_path):

    output = tmp_path / "features.csv"

    df = pd.DataFrame(
        {
            "smiles": ["CCO"],
            "activity": [1]
        }
    )

    save_features(df, output)

    assert output.exists()
