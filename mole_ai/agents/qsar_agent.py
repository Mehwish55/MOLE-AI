"""
MOLE-AI v2 QSAR Prediction Agent.

Provides a clean agent interface around the existing
trained QSAR model.
"""

from mole_ai.models.predict import predict_from_smiles


class QSARAgent:
    """
    Agent responsible for molecular activity prediction.
    """

    def predict(self, smiles: str) -> dict:
        """
        Predict molecular activity (pIC50) from SMILES.

        Parameters
        ----------
        smiles : str
            Molecular SMILES representation.

        Returns
        -------
        dict
            Structured prediction result.
        """

        if not isinstance(smiles, str):
            raise TypeError("SMILES must be a string.")

        smiles = smiles.strip()

        if not smiles:
            raise ValueError("SMILES string cannot be empty.")

        prediction = predict_from_smiles(smiles)

        if prediction is None:
            raise ValueError(
                f"Invalid SMILES string: {smiles}"
            )

        if prediction >= 7:
            activity = "High Activity"
        elif prediction >= 5:
            activity = "Moderate Activity"
        else:
            activity = "Low Activity"

        return {
            "smiles": smiles,
            "predicted_pIC50": round(prediction, 3),
            "activity_class": activity,
            "model": "Random Forest",
        }
