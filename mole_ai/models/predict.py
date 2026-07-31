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
from pathlib import Path
import joblib
import numpy as np

from rdkit import Chem
from rdkit.DataStructs import ConvertToNumpyArray

from mole_ai.features.fingerprints import (
    generate_fingerprint
)

MODEL_PATH = (
    Path(__file__).resolve().parent
    / "qsar_random_forest.pkl"
)

def load_model():

    if not MODEL_PATH.exists():
        st.error(f"Model file not found: {MODEL_PATH}")
        return None

    return joblib.load(MODEL_PATH)

def predict_from_smiles(smiles):
    """
    Predict pIC50 directly from SMILES.
    """

    mol = Chem.MolFromSmiles(
        smiles
    )

    if mol is None:
      return None


    fingerprint = generate_fingerprint(
        mol
    )


    features = np.zeros(
        (2048,)
    )


    ConvertToNumpyArray(
        fingerprint,
        features
    )


    model = load_model()

    if model is None:
          return None

    prediction = model.predict(
         [features]
   )


    return float(
        prediction[0]
    )
