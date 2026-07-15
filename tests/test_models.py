import pandas as pd

from mole_ai.models.train import load_feature_dataset


def test_load_feature_dataset(tmp_path):

    sample = tmp_path / "features.csv"

    df = pd.DataFrame(
        {
            "feature1": [1, 2],
            "activity": [7.1, 6.8]
        }
    )

    df.to_csv(sample, index=False)

    loaded = load_feature_dataset(sample)

    assert len(loaded) == 2
    assert "activity" in loaded.columns


from mole_ai.models.train import prepare_training_data


def test_prepare_training_data():

    df = pd.DataFrame(
        {
            "smiles": ["CCO", "CCC"],
            "mw": [46.07, 44.09],
            "logp": [-0.1, 1.4],
            "activity": [7.2, 6.5]
        }
    )

    X, y = prepare_training_data(df)

    assert "activity" not in X.columns
    assert "smiles" not in X.columns
    assert len(X) == 2
    assert len(y) == 2
