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

from mole_ai.models.train import train_random_forest


def test_train_random_forest():

    df = pd.DataFrame(
        {
            "mw": [46.07, 44.09, 60.10, 75.20],
            "logp": [-0.1, 1.4, 0.5, 2.0],
            "pIC50": [7.2, 6.5, 8.1, 5.9],
        }
    )

    X = df.drop(columns=["pIC50"])
    y = df["pIC50"]

    model, X_test, y_test = train_random_forest(X, y)

    assert model is not None
    assert len(X_test) > 0
    assert len(y_test) > 0
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
