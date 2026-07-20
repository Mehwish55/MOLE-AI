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

    return pd.Series(
        predictions,
        name="predicted_pIC50",
    )


def predict_batch(
    model,
    dataframe: pd.DataFrame,
    feature_columns,
    id_column="smiles",
):
    """
    Generate predictions for a batch of molecules.

    Parameters
    ----------
    model :
        Trained machine learning model.

    dataframe : pandas.DataFrame
        Dataset containing molecule information and features.

    feature_columns : list
        Columns used for prediction.

    id_column : str
        Molecule identifier column.

    Returns
    -------
    pandas.DataFrame
        Molecule identifiers with predictions.
    """

    features = dataframe[feature_columns]

    predictions = model.predict(features)

    result = pd.DataFrame(
        {
            id_column: dataframe[id_column],
            "predicted_pIC50": predictions,
        }
    )

    return result

def save_predictions(
    predictions,
    output_path,
):
    """
    Save prediction results to CSV.

    Parameters
    ----------
    predictions :
        Prediction dataframe.

    output_path : str
        Output CSV file path.

    Returns
    -------
    str
        Saved file path.
    """

    predictions.to_csv(
        output_path,
        index=False,
    )

    return output_path
