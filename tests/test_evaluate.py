import pandas as pd

from mole_ai.models.train import train_random_forest
from mole_ai.models.evaluate import evaluate_regression


def test_evaluate_regression():

    df = pd.DataFrame(
        {
            "mw": [46.07, 44.09, 60.10, 75.20, 80.30, 95.40, 101.50, 110.20, 125.00, 140.30],
            "logp": [-0.1, 1.4, 0.5, 2.0, 1.8, 2.3, 1.1, 0.8, 2.7, 3.0],
            "activity": [7.2, 6.5, 8.1, 5.9, 7.5, 6.8, 7.9, 8.3, 5.7, 6.9],
        }
    )

    X = df.drop(columns=["activity"])
    y = df["activity"]

    model, X_test, y_test = train_random_forest(X, y)

    metrics = evaluate_regression(model, X_test, y_test)

    assert "r2" in metrics
    assert "rmse" in metrics
    assert "mae" in metrics
