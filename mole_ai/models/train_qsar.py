"""
Train Random Forest QSAR model.
"""

import pandas as pd
import joblib

from rdkit import Chem
from rdkit.DataStructs import ConvertToNumpyArray

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score
)

import numpy as np

from mole_ai.features.fingerprints import (
    generate_fingerprint
)


# Load dataset

DATA_PATH = "data/qsar_dataset.csv"


df = pd.read_csv(DATA_PATH)


X = []
y = []


# Convert SMILES into fingerprints

for smiles, activity in zip(
    df["SMILES"],
    df["pIC50"]
):

    mol = Chem.MolFromSmiles(smiles)

    if mol:

        fp = generate_fingerprint(mol)

        arr = np.zeros((2048,))

        ConvertToNumpyArray(
            fp,
            arr
        )

        X.append(arr)
        y.append(activity)



X = np.array(X)
y = np.array(y)



# Split dataset

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)



# Train model

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


model.fit(
    X_train,
    y_train
)



# Evaluation

predictions = model.predict(
    X_test
)


r2 = r2_score(
    y_test,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions
    )
)


mae = mean_absolute_error(
    y_test,
    predictions
)


print("\nModel Performance")
print("----------------------")

print(
    "R2:",
    round(r2,3)
)

print(
    "RMSE:",
    round(rmse,3)
)

print(
    "MAE:",
    round(mae,3)
)



# Save model

MODEL_PATH = (
    "mole_ai/models/"
    "qsar_random_forest.pkl"
)


joblib.dump(
    model,
    MODEL_PATH
)


print("\nModel saved:")
print(MODEL_PATH)
