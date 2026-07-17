import pandas as pd

from sklearn.ensemble import RandomForestRegressor

from mole_ai.models.train import tune_random_forest


def test_tune_random_forest():

    df = pd.DataFrame(
        {
            "feature1": [1, 2, 3, 4, 5, 6, 7, 8],
            "feature2": [8, 7, 6, 5, 4, 3, 2, 1],
            "activity": [10, 20, 30, 40, 50, 60, 70, 80],
        }
    )

    X = df[["feature1", "feature2"]]
    y = df["activity"]

    model = tune_random_forest(
        X,
        y,
    )

    assert isinstance(
        model,
        RandomForestRegressor,
    )
