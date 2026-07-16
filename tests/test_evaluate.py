import pandas as pd

from mole_ai.models.train import train_random_forest
from mole_ai.models.evaluate import evaluate_regression


def test_evaluate_regression():

    df = pd.DataFrame(
        {
            "mw": [
                46.07,
                44.09,
                60.10,
                75.20,
                80.30,
                90.10,
                55.20,
                70.40,
                65.30,
                88.60,
            ],
            "logp": [
                -0.1,
                1.4,
                0.5,
                2.0,
                1.8,
                1.2,
                0.3,
                1.6,
                0.8,
                2.1,
            ],
            "activity": [
                7.2,
                6.5,
                8.1,
                5.9,
                7.5,
                6.9,
                8.0,
                6.2,
                7.7,
                6.1,
            ],
        }
    )

    X = df.drop(columns=["activity"])
    y = df["activity"]

    model, X_test, y_test = train_random_forest(X, y)

    metrics = evaluate_regression(
        model,
        X_test,
        y_test,
    )

    assert "mae" in metrics
    assert "rmse" in metrics
    assert "r2" in metrics
