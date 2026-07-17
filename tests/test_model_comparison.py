import pandas as pd

from mole_ai.models.train import train_models


def test_train_multiple_models():

    df = pd.DataFrame(
        {
            "feature1": [1, 2, 3, 4, 5],
            "feature2": [5, 4, 3, 2, 1],
            "activity": [10, 20, 30, 40, 50],
        }
    )

    X = df.drop(columns=["activity"])
    y = df["activity"]

    models, X_test, y_test = train_models(X, y)

    assert "Linear Regression" in models
    assert "Random Forest" in models
    assert "Gradient Boosting" in models

    assert len(X_test) > 0
    assert len(y_test) > 0
