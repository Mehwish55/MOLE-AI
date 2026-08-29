"""
MOLE-AI v2 Molecular Similarity Agent.

Calculates molecular similarity using Morgan fingerprints
and Tanimoto similarity.
"""

from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs


class SimilarityAgent:
    """
    Molecular similarity analysis agent.

    Uses Morgan fingerprints and Tanimoto similarity
    to compare molecules.
    """

    def __init__(self, radius: int = 2, n_bits: int = 2048):
        self.radius = radius
        self.n_bits = n_bits

    def _fingerprint(self, smiles: str):
        """Generate Morgan fingerprint for a SMILES string."""

        molecule = Chem.MolFromSmiles(smiles)

        if molecule is None:
            raise ValueError(
                f"Invalid SMILES string: {smiles}"
            )

        return AllChem.GetMorganFingerprintAsBitVect(
            molecule,
            self.radius,
            nBits=self.n_bits,
        )

    def calculate_similarity(
        self,
        query_smiles: str,
        target_smiles: str,
    ) -> float:
        """
        Calculate Tanimoto similarity between two molecules.
        """

        query_fp = self._fingerprint(query_smiles)
        target_fp = self._fingerprint(target_smiles)

        similarity = DataStructs.TanimotoSimilarity(
            query_fp,
            target_fp,
        )

        return round(float(similarity), 4)

    def rank_similar(
        self,
        query_smiles: str,
        library: list[dict],
        top_k: int = 10,
    ) -> list[dict]:
        """
        Rank molecules in a library by similarity.

        Expected library format:

        [
            {
                "compound_id": "Compound_001",
                "smiles": "CCO"
            }
        ]
        """

        query_fp = self._fingerprint(query_smiles)

        results = []

        for compound in library:

            smiles = compound.get("smiles")

            if not smiles:
                continue

            molecule = Chem.MolFromSmiles(smiles)

            if molecule is None:
                continue

            target_fp = AllChem.GetMorganFingerprintAsBitVect(
                molecule,
                self.radius,
                nBits=self.n_bits,
            )

            similarity = DataStructs.TanimotoSimilarity(
                query_fp,
                target_fp,
            )

            results.append(
                {
                    "compound_id": compound.get(
                        "compound_id",
                        "Unknown",
                    ),
                    "smiles": smiles,
                    "similarity": round(
                        float(similarity),
                        4,
                    ),
                }
            )

        results.sort(
            key=lambda x: x["similarity"],
            reverse=True,
        )

        return results[:top_k]
