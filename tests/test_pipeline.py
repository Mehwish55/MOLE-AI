import pandas as pd

from mole_ai.data.chembl import prepare_chembl_dataset
from mole_ai.features.builder import build_feature_matrix


def test_chembl_feature_pipeline():

    df = pd.DataFrame(
        {
            "smiles": ["CCO", "CCC"],
            "IC50": [100, 10],
        }
    )

    cleaned = prepare_chembl_dataset(df)

    features = build_feature_matrix(cleaned)

    assert len(features) == 2
    assert "pIC50" in cleaned.columns
