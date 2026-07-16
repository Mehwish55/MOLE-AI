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


from mole_ai.data.chembl import ic50_to_pic50


def test_ic50_to_pic50():

    result = ic50_to_pic50(100)

    assert round(result, 2) == 7.00


from mole_ai.data.chembl import prepare_chembl_dataset


def test_prepare_chembl_dataset():

    df = pd.DataFrame(
        {
            "smiles": ["CCO", "CCC"],
            "IC50": [100, 10],
        }
    )

    cleaned = prepare_chembl_dataset(df)

    assert "pIC50" in cleaned.columns
    assert len(cleaned) == 2
