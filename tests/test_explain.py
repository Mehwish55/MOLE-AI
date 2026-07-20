import pandas as pd

from sklearn.ensemble import RandomForestRegressor

from mole_ai.models.explain import get_feature_importance


def test_feature_importance():

    X = pd.DataFrame(
        {
            "feature1": [1, 2, 3, 4],
            "feature2": [4, 3, 2, 1],
        }
    )

    y = [10, 20, 30, 40]

    model = RandomForestRegressor(
        n_estimators=10,
        random_state=42,
    )

    model.fit(X, y)

    result = get_feature_importance(
        model,
        X.columns,
    )

    assert len(result) == 2
    assert "feature" in result.columns
    assert "importance" in result.columns
