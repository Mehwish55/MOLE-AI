import pandas as pd

from mole_ai.models.predict import predict_batch


class DummyModel:

    def predict(self, X):
        return [5.1, 6.2, 7.3]


def test_predict_batch():

    df = pd.DataFrame(
        {
            "smiles": [
                "CCO",
                "CCCO",
                "CCN",
            ],
            "feature_1": [
                1,
                2,
                3,
            ],
            "feature_2": [
                4,
                5,
                6,
            ],
        }
    )

    model = DummyModel()

    result = predict_batch(
        model,
        df,
        [
            "feature_1",
            "feature_2",
        ],
    )

    assert len(result) == 3

    assert "smiles" in result.columns

    assert "predicted_pIC50" in result.columns

    assert result.iloc[0]["predicted_pIC50"] == 5.1
