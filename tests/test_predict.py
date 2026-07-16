import pandas as pd

from mole_ai.models.train import train_random_forest
from mole_ai.models.predict import predict_from_dataframe


def test_predict_from_dataframe():

    df = pd.DataFrame(
        {
            "mw": [46.07, 44.09, 60.10, 75.20, 80.30],
            "logp": [-0.1, 1.4, 0.5, 2.0, 1.8],
            "activity": [7.2, 6.5, 8.1, 5.9, 7.5],
        }
    )

    X = df.drop(columns=["activity"])
    y = df["activity"]

    model, _, _ = train_random_forest(X, y)

    predictions = predict_from_dataframe(model, X)

    assert len(predictions) == len(X)
    assert predictions.name == "predicted_pIC50"
