"""
Prediction utilities for MOLE-AI.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from rdkit import Chem
from rdkit.DataStructs import ConvertToNumpyArray

from mole_ai.features.fingerprints import generate_fingerprint


MODEL_PATH = (
    Path(__file__).resolve().parent
    / "qsar_random_forest.pkl"
)


def load_model():
    """
    Load the trained QSAR model.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def predict(model, features):
    """
    Generate predictions using a trained model.
    """

    return model.predict(features)


def predict_from_dataframe(
    model,
    feature_df: pd.DataFrame,
):
    """
    Predict pIC50 values from a feature DataFrame.
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
    """

    features = dataframe[feature_columns]

    predictions = model.predict(features)

    return pd.DataFrame(
        {
            id_column: dataframe[id_column],
            "predicted_pIC50": predictions,
        }
    )


def predict_from_smiles(smiles):
    """
    Predict pIC50 directly from a SMILES string.
    """

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None

    fingerprint = generate_fingerprint(mol)

    features = np.zeros(
        (2048,),
        dtype=np.float64,
    )

    ConvertToNumpyArray(
        fingerprint,
        features,
    )

    model = load_model()

    prediction = model.predict(
        [features]
    )

    return float(prediction[0])
