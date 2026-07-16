"""
Evaluation utilities for regression models.
"""

import math

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


def evaluate_regression(model, X_test, y_test):
    """
    Evaluate a regression model.
    """

    predictions = model.predict(X_test)

    metrics = {
        "r2": r2_score(y_test, predictions),
        "rmse": math.sqrt(mean_squared_error(y_test, predictions)),
        "mae": mean_absolute_error(y_test, predictions),
    }

    return metrics
