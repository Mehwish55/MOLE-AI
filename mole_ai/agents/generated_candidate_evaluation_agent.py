"""
MOLE-AI v2 Generated Candidate Evaluation Agent.

Evaluates generated molecular candidates using:
- molecular similarity
- QSAR activity prediction
- ADMET analysis
- candidate ranking

This agent provides transparent computational prioritization.
It does not represent experimentally validated compounds.
"""
from mole_ai.agents.chemistry_agent import ChemistryAgent
from mole_ai.agents.qsar_agent import QSARAgent
from mole_ai.agents.admet_agent import ADMETAgent
from mole_ai.ranking.candidate_ranker import CandidateRanker


class GeneratedCandidateEvaluationAgent:
    """
    Evaluate generated molecular candidates using existing
    MOLE-AI analysis components.
    """

    def __init__(self):
        self.chemistry_agent = ChemistryAgent()
        self.qsar_agent = QSARAgent()
        self.admet_agent = ADMETAgent()
        self.candidate_ranker = CandidateRanker()

    def evaluate_candidate(
        self,
        candidate: dict,
    ) -> dict:
        """
        Evaluate one generated molecular candidate.

        Parameters
        ----------
        candidate : dict
            Generated candidate containing at least a SMILES string.

        Returns
        -------
        dict
            Computational evaluation results.
        """

        smiles = candidate.get("smiles")

        if not smiles:
            raise ValueError(
                "Generated candidate must contain a SMILES string."
            )

        chemistry_result = self.chemistry_agent.analyze(smiles)
        qsar_result = self.qsar_agent.predict(smiles)

        admet_result = self.admet_agent.analyze(smiles)

        workflow_result = {
            "smiles": smiles,
            "chemistry": chemistry_result,
            "qsar": qsar_result,
            "admet": admet_result,
        }

        ranking_result = self.candidate_ranker.rank(
            workflow_result
        )

        return {
            "candidate_id": candidate.get(
                "candidate_id",
                "UNKNOWN",
            ),
            "smiles": smiles,
            "strategy": candidate.get(
                "strategy",
                "Unknown",
            ),
            "similarity": float(
                candidate.get("similarity", 0.0)
            ),
            "predicted_pIC50": qsar_result[
                "predicted_pIC50"
            ],
            "activity_class": qsar_result.get(
                "activity_class",
                "Unknown",
            ),
            "admet_score": admet_result[
                "admet_score"
            ],
            "overall_score": ranking_result[
                "overall_score"
            ],
            "priority": ranking_result.get(
                "priority",
                "Unknown",
            ),
        }

    def evaluate_candidates(
        self,
        candidates: list[dict],
    ) -> list[dict]:
        """
        Evaluate multiple generated candidates.

        Invalid candidates are skipped rather than stopping
        evaluation of the remaining candidates.
        """

        evaluated_candidates = []

        for candidate in candidates:

            try:
                evaluation = self.evaluate_candidate(
                    candidate
                )

                evaluated_candidates.append(
                    evaluation
                )

            except Exception:
                continue

        evaluated_candidates.sort(
            key=lambda item: item["overall_score"],
            reverse=True,
        )

        return evaluated_candidates
