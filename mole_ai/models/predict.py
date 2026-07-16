"""
Prediction utilities for MOLE-AI.
"""


def predict(model, features):
    """
    Generate predictions using a trained model.

    Parameters
    ----------
    model :
        Trained machine learning model.

    features :
        Feature matrix for molecules.

    Returns
    -------
    predictions :
        Predicted pIC50 values.
    """

    return model.predict(features)


def save_predictions(predictions, output_path):
    """
    Save predicted pIC50 values to a CSV file.

    Parameters
    ----------
    predictions : pandas.Series
        Predicted pIC50 values.

    output_path : str
        Output CSV file path.
    """

    predictions.to_frame().to_csv(output_path, index=False)
import pandas as pd


def predict_from_dataframe(model, feature_df: pd.DataFrame):
    """
    Predict pIC50 values from a feature DataFrame.

    Parameters
    ----------
    model :
        Trained machine learning model.

    feature_df : pandas.DataFrame
        Molecular feature matrix.

    Returns
    -------
    pandas.Series
        Predicted pIC50 values.
    """

    predictions = model.predict(feature_df)

    return pd.Series(predictions, name="predicted_pIC50")
