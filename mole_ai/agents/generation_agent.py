"""
MOLE-AI v2 Molecular Generation Agent.

Generates transparent, rule-based molecular variants from
a parent molecule using controlled structural transformations.

This module is intended for computational hypothesis generation
and does not represent experimentally validated compounds.
"""

from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs


class MolecularGenerationAgent:
    """
    Generate controlled molecular variants from a parent molecule.

    The first implementation uses simple, interpretable
    transformations rather than an opaque generative model.
    """

    def __init__(self, radius: int = 2, n_bits: int = 2048):
        self.radius = radius
        self.n_bits = n_bits

    def _validate_smiles(self, smiles: str):
        """Validate and return an RDKit molecule."""
        molecule = Chem.MolFromSmiles(smiles)

        if molecule is None:
            raise ValueError(
                f"Invalid SMILES string: {smiles}"
            )

        return molecule

    def _similarity(
        self,
        parent_molecule,
        candidate_molecule,
    ) -> float:
        """Calculate Morgan fingerprint Tanimoto similarity."""

        parent_fp = AllChem.GetMorganFingerprintAsBitVect(
            parent_molecule,
            self.radius,
            nBits=self.n_bits,
        )

        candidate_fp = AllChem.GetMorganFingerprintAsBitVect(
            candidate_molecule,
            self.radius,
            nBits=self.n_bits,
        )

        similarity = DataStructs.TanimotoSimilarity(
            parent_fp,
            candidate_fp,
        )

        return round(float(similarity), 4)

    def generate_candidates(
        self,
        smiles: str,
        max_candidates: int = 10,
    ) -> list[dict]:
        """
        Generate simple molecular variants.

        Returns validated candidate molecules together with
        their generation strategy and similarity to the parent.
        """

        parent = self._validate_smiles(smiles)

        candidates = []

        # --------------------------------------------------
        # Transformation 1 — Remove explicit hydrogens
        # --------------------------------------------------

        base_smiles = Chem.MolToSmiles(parent)

        candidates.append(
            {
                "candidate_id": "GEN_001",
                "smiles": base_smiles,
                "strategy": "Canonicalization",
                "similarity": 1.0,
            }
        )

        # --------------------------------------------------
        # Transformation 2 — Controlled methyl substitution
        # --------------------------------------------------

        methyl_reaction = AllChem.ReactionFromSmarts(
            "[cH:1]>>[c:1]C"
        )

        try:
            products = methyl_reaction.RunReactants(
                (parent,)
            )

            for index, product_set in enumerate(products):

                if len(candidates) >= max_candidates:
                    break

                product = product_set[0]

                try:
                    Chem.SanitizeMol(product)
                except Exception:
                    continue

                candidate_smiles = Chem.MolToSmiles(
                    product,
                    canonical=True,
                )

                candidates.append(
                    {
                        "candidate_id": f"GEN_{len(candidates) + 1:03d}",
                        "smiles": candidate_smiles,
                        "strategy": "Aromatic methyl substitution",
                        "similarity": self._similarity(
                            parent,
                            product,
                        ),
                    }
                )

        except Exception:
            pass

        # --------------------------------------------------
        # Remove duplicate molecules
        # --------------------------------------------------

        unique = {}

        for candidate in candidates:
            unique[candidate["smiles"]] = candidate

        candidates = list(unique.values())

        # --------------------------------------------------
        # Similarity ranking
        # --------------------------------------------------

        candidates.sort(
            key=lambda item: item["similarity"],
            reverse=True,
        )

        return candidates[:max_candidates]
