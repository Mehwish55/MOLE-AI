from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


"""
Model training utilities for MOLE-AI.
"""

import pandas as pd


def load_feature_dataset(file_path: str) -> pd.DataFrame:

def prepare_training_data(df: pd.DataFrame):
def train_random_forest(X, y):
    """
    Train a Random Forest regression model.

    Parameters
    ----------
    X : pandas.DataFrame
        Feature matrix.

    y : pandas.Series
        Target values (pIC50).

    Returns
    -------
    model
        Trained Random Forest model.
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



    """
    Split dataset into features (X) and target (y).

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    tuple
        X, y
    """

    X = df.drop(columns=["activity"])

    if "smiles" in X.columns:
        X = X.drop(columns=["smiles"])

    y = df["activity"]

    return X, y


    """
    Load the engineered feature dataset.

    Parameters
    ----------
    file_path : str
        Path to the feature CSV.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset.
    """
    return pd.read_csv(file_path)
