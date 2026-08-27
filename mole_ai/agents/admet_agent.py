"""
MOLE-AI v2 ADMET Agent.

Provides drug-likeness and physicochemical screening
using the existing MOLE-AI ADMET utilities.
"""

from mole_ai.admet import (
    calculate_admet,
    lipinski_check,
    admet_score,
)


class ADMETAgent:
    """
    Agent responsible for ADMET-related molecular screening.
    """

    def analyze(self, smiles: str) -> dict:
        """
        Analyze ADMET-related molecular properties.

        Parameters
        ----------
        smiles : str
            Molecular SMILES representation.

        Returns
        -------
        dict
            Structured ADMET analysis.
        """

        if not isinstance(smiles, str):
            raise TypeError("SMILES must be a string.")

        smiles = smiles.strip()

        if not smiles:
            raise ValueError("SMILES string cannot be empty.")

        properties = calculate_admet(smiles)

        if properties is None:
            raise ValueError(
                f"Invalid SMILES string: {smiles}"
            )

        drug_likeness = lipinski_check(properties)
        score = admet_score(properties)

        return {
            "smiles": smiles,
            "properties": properties,
            "drug_likeness": drug_likeness,
            "admet_score": score,
        }
