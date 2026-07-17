import pandas as pd

from mole_ai.models.train import train_models
from mole_ai.models.evaluate import compare_models


def test_compare_models():

    df = pd.DataFrame(
        {
            "feature1": [1, 2, 3, 4, 5, 6],
            "feature2": [6, 5, 4, 3, 2, 1],
            "activity": [10, 20, 30, 40, 50, 60],
        }
    )

    X = df.drop(columns=["activity"])
    y = df["activity"]

    models, X_test, y_test = train_models(X, y)

    results = compare_models(
        models,
        X_test,
        y_test,
    )

    assert len(results) == 3

    assert "model" in results.columns
    assert "mae" in results.columns
    assert "rmse" in results.columns
    assert "r2" in results.columns

    assert results.iloc[0]["rmse"] <= results.iloc[-1]["rmse"]
