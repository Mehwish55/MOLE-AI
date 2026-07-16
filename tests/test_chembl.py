import pandas as pd

from mole_ai.data.chembl import filter_activity_data


def test_filter_activity_data():

    df = pd.DataFrame(
        {
            "smiles": ["CCO", None, "CCC"],
            "IC50": [100, 200, None],
        }
    )

    cleaned = filter_activity_data(df)

    assert len(cleaned) == 1
    assert "smiles" in cleaned.columns
    assert "IC50" in cleaned.columns
