import pandas as pd

from sklearn.ensemble import RandomForestRegressor

from mole_ai.models.train import cross_validate_model


def test_cross_validate_model():

    df = pd.DataFrame(
        {
            "feature1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "feature2": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
            "activity": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
        }
    )

    X = df[["feature1", "feature2"]]
    y = df["activity"]

    model = RandomForestRegressor(
        n_estimators=10,
        random_state=42,
    )

    score = cross_validate_model(
        model,
        X,
        y,
    )

    assert isinstance(score, float)
