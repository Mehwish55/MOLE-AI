"""
MOLE-AI v2 Drug Discovery Workflow.

Coordinates the Chemistry, QSAR, ADMET, and Candidate
Ranking components into a unified molecular analysis workflow.
"""

from mole_ai.agents.chemistry_agent import ChemistryAgent
from mole_ai.agents.qsar_agent import QSARAgent
from mole_ai.agents.admet_agent import ADMETAgent
from mole_ai.ranking.candidate_ranker import CandidateRanker


class DrugDiscoveryWorkflow:
    """
    Orchestrates the MOLE-AI v2 molecular analysis pipeline.
    """

    def __init__(self):
        self.chemistry_agent = ChemistryAgent()
        self.qsar_agent = QSARAgent()
        self.admet_agent = ADMETAgent()
        self.candidate_ranker = CandidateRanker()

    def analyze(self, smiles: str) -> dict:
        """
        Run the complete molecular discovery workflow.

        Parameters
        ----------
        smiles : str
            Molecular SMILES representation.

        Returns
        -------
        dict
            Combined analysis from all components.
        """

        # 1. Chemistry analysis
        chemistry_result = self.chemistry_agent.analyze(smiles)

        # 2. QSAR prediction
        qsar_result = self.qsar_agent.predict(smiles)

        # 3. ADMET analysis
        admet_result = self.admet_agent.analyze(smiles)

        # Combine results before ranking
        workflow_result = {
            "smiles": smiles,
            "chemistry": chemistry_result,
            "qsar": qsar_result,
            "admet": admet_result,
        }

        # 4. Candidate prioritization
        ranking_result = self.candidate_ranker.rank(
            workflow_result
        )

        # 5. Add ranking to final result
        workflow_result["ranking"] = ranking_result

        return workflow_result
