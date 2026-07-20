import pandas as pd

from mole_ai.models.train import train_random_forest
from mole_ai.models.predict import predict


def test_prediction():

    df = pd.DataFrame(
        {
            "mw": [46.07, 44.09, 60.10, 75.20, 80.30, 95.40],
            "logp": [-0.1, 1.4, 0.5, 2.0, 1.8, 2.3],
            "activity": [7.2, 6.5, 8.1, 5.9, 7.5, 6.8],
        }
    )

    X = df.drop(columns=["activity"])
    y = df["activity"]

    model, _, _ = train_random_forest(X, y)

    new_features = pd.DataFrame(
        {
            "mw": [50.0],
            "logp": [1.0],
        }
    )

    result = predict(model, new_features)

    assert len(result) == 1
