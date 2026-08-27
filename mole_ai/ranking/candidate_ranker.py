"""
MOLE-AI v2 Candidate Ranking.

Combines model activity and drug-likeness information
into a computational candidate prioritization score.
"""


class CandidateRanker:
    """
    Rank molecules using a transparent scoring framework.
    """

    def rank(self, workflow_result: dict) -> dict:
        """
        Calculate a candidate prioritization score.

        Parameters
        ----------
        workflow_result : dict
            Combined output from DrugDiscoveryWorkflow.

        Returns
        -------
        dict
            Candidate ranking result.
        """

        qsar = workflow_result["qsar"]
        admet = workflow_result["admet"]

        predicted_pic50 = qsar["predicted_pIC50"]
        admet_score = admet["admet_score"]

        # Activity score
        if predicted_pic50 >= 8:
            activity_score = 100
        elif predicted_pic50 >= 7:
            activity_score = 90
        elif predicted_pic50 >= 6:
            activity_score = 75
        elif predicted_pic50 >= 5:
            activity_score = 60
        else:
            activity_score = 40

        # Transparent weighted score
        overall_score = (
            0.6 * activity_score
            + 0.4 * admet_score
        )

        overall_score = round(overall_score, 2)

        if overall_score >= 80:
            priority = "High Priority"
        elif overall_score >= 60:
            priority = "Medium Priority"
        else:
            priority = "Low Priority"

        return {
            "activity_score": activity_score,
            "admet_score": admet_score,
            "overall_score": overall_score,
            "priority": priority,
        }
