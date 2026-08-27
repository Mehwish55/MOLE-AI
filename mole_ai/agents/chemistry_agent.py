"""
MOLE-AI v2 Chemistry Agent.

Responsible for validating molecules and generating
standardized molecular analysis results.
"""

from rdkit.Chem import Draw

from mole_ai.chem.smiles import (
    smiles_to_mol,
    validate_smiles,
)

from mole_ai.chem.descriptors import (
    calculate_descriptors,
)

from mole_ai.chem.fingerprints import (
    generate_morgan_fingerprint,
)


class ChemistryAgent:
    """
    AI-ready chemistry analysis agent.

    Converts a SMILES string into a structured
    molecular analysis result.
    """

    def analyze(self, smiles: str) -> dict:
        """
        Analyze a molecule from a SMILES string.

        Parameters
        ----------
        smiles : str
            Molecular SMILES representation.

        Returns
        -------
        dict
            Structured molecular analysis.
        """

        if not isinstance(smiles, str):
            raise TypeError("SMILES must be a string.")

        smiles = smiles.strip()

        if not smiles:
            raise ValueError("SMILES string cannot be empty.")

        if not validate_smiles(smiles):
            raise ValueError(
                f"Invalid SMILES string: {smiles}"
            )

        mol = smiles_to_mol(smiles)

        descriptors = calculate_descriptors(mol)

        fingerprint = generate_morgan_fingerprint(mol)

        lipinski_pass = (
            descriptors["molecular_weight"] <= 500
            and descriptors["logp"] <= 5
            and descriptors["hbd"] <= 5
            and descriptors["hba"] <= 10
        )

        return {
            "smiles": smiles,
            "valid": True,
            "descriptors": descriptors,
            "fingerprint": fingerprint,
            "fingerprint_size": len(fingerprint),
            "lipinski_pass": lipinski_pass,
        }
