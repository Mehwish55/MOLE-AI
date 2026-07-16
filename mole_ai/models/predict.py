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
