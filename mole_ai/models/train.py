"""
Model training utilities for MOLE-AI.
"""

import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV


def load_feature_dataset(file_path: str) -> pd.DataFrame:
    """
    Load the engineered feature dataset.
    """
    return pd.read_csv(file_path)


def prepare_training_data(df: pd.DataFrame):
    """
    Split dataset into features (X) and target (y).
    """

    X = df.drop(columns=["activity"])

    if "smiles" in X.columns:
        X = X.drop(columns=["smiles"])

    y = df["activity"]

    return X, y


def train_random_forest(X, y):
    """
    Train a Random Forest regression model.
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
    )

    model.fit(X_train, y_train)

    return model, X_test, y_test


def train_models(X, y):
    """
    Train multiple regression models.
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=100,
            random_state=42,
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            random_state=42,
        ),
    }

    trained_models = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        trained_models[name] = model

    return trained_models, X_test, y_test


def cross_validate_model(model, X, y):
    """
    Perform cross-validation for a regression model.
    """

    scores = cross_val_score(
        model,
        X,
        y,
        cv=5,
        scoring="r2",
    )

    return scores.mean()


def tune_random_forest(X, y):
    """
    Tune Random Forest hyperparameters.
    """

    model = RandomForestRegressor(
        random_state=42,
    )

    parameters = {
        "n_estimators": [50, 100],
        "max_depth": [None, 5],
    }

    search = GridSearchCV(
        model,
        parameters,
        cv=3,
        scoring="r2",
    )

    search.fit(X, y)

    return search.best_estimator_
