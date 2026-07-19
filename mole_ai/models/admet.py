"""
ADMET prediction utilities for MOLE-AI.
"""

import pandas as pd


def predict_admet(model, features):
    """
    Predict ADMET properties.

    Parameters
    ----------
    model :
        Trained ADMET prediction model.

    features :
        Molecular feature matrix.

    Returns
    -------
    pandas.DataFrame
        Predicted ADMET values.
    """

    predictions = model.predict(features)

    return pd.DataFrame(
        predictions,
        columns=[
            "admet_prediction"
        ],
    )


def create_admet_profile(predictions):
    """
    Create molecular ADMET profile.

    Parameters
    ----------
    predictions :
        ADMET prediction values.

    Returns
    -------
    dict
        ADMET profile.
    """

    return {
        "toxicity": predictions.get("toxicity"),
        "solubility": predictions.get("solubility"),
        "lipophilicity": predictions.get("lipophilicity"),
        "bbb_permeability": predictions.get(
            "bbb_permeability"
        ),
    }
