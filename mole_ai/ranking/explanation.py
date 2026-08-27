"""
MOLE-AI v2 Candidate Explainability.

Generates human-readable explanations for
molecular candidate prioritization.
"""


class CandidateExplainer:
    """
    Explain why a molecule received its ranking.
    """

    def explain(self, result: dict) -> dict:
        """
        Generate an explanation from workflow results.

        Parameters
        ----------
        result : dict
            Output from DrugDiscoveryWorkflow.

        Returns
        -------
        dict
            Structured candidate explanation.
        """

        smiles = result["smiles"]

        qsar = result["qsar"]
        admet = result["admet"]
        ranking = result["ranking"]

        predicted_pic50 = float(
            qsar["predicted_pIC50"]
        )

        activity_class = qsar[
            "activity_class"
        ]

        activity_score = float(
            ranking["activity_score"]
        )

        admet_score = float(
            ranking["admet_score"]
        )

        overall_score = float(
            ranking["overall_score"]
        )

        priority = ranking[
            "priority"
        ]

        drug_likeness = admet[
            "drug_likeness"
        ]

        # --------------------------------------------------
        # Activity interpretation
        # --------------------------------------------------

        if predicted_pic50 >= 7:

            activity_explanation = (
                "Strong predicted molecular activity."
            )

        elif predicted_pic50 >= 5:

            activity_explanation = (
                "Moderate predicted molecular activity."
            )

        else:

            activity_explanation = (
                "Lower predicted molecular activity."
            )

        # --------------------------------------------------
        # ADMET interpretation
        # --------------------------------------------------

        if admet_score >= 80:

            admet_explanation = (
                "Favorable drug-likeness and ADMET profile."
            )

        elif admet_score >= 60:

            admet_explanation = (
                "Acceptable ADMET profile with some limitations."
            )

        else:

            admet_explanation = (
                "ADMET profile shows potential liabilities."
            )

        # --------------------------------------------------
        # Overall interpretation
        # --------------------------------------------------

        if overall_score >= 80:

            overall_explanation = (
                "Strong candidate for further computational evaluation."
            )

        elif overall_score >= 60:

            overall_explanation = (
                "Reasonable candidate that may benefit from further optimization."
            )

        else:

            overall_explanation = (
                "Lower-priority candidate for further investigation."
            )

        # --------------------------------------------------
        # Recommendation
        # --------------------------------------------------

        if priority == "High Priority":

            recommendation = (
                "Prioritize for downstream computational studies "
                "such as molecular docking and further ADMET evaluation."
            )

        elif priority == "Medium Priority":

            recommendation = (
                "Consider for further optimization and computational "
                "validation before experimental testing."
            )

        else:

            recommendation = (
                "Lower priority; consider molecular optimization "
                "before additional downstream analysis."
            )

        # --------------------------------------------------
        # Final explanation
        # --------------------------------------------------

        summary = (
            f"The molecule has a predicted pIC50 of "
            f"{predicted_pic50:.3f}, classified as "
            f"{activity_class}. It received an activity score "
            f"of {activity_score:.1f}/100 and an ADMET score "
            f"of {admet_score:.1f}/100, resulting in an overall "
            f"candidate score of {overall_score:.1f}/100 and "
            f"a final priority of {priority}."
        )

        return {
            "smiles": smiles,

            "activity": {
                "predicted_pIC50": predicted_pic50,
                "classification": activity_class,
                "score": activity_score,
                "interpretation": activity_explanation,
            },

            "admet": {
                "score": admet_score,
                "drug_likeness": drug_likeness,
                "interpretation": admet_explanation,
            },

            "ranking": {
                "overall_score": overall_score,
                "priority": priority,
                "interpretation": overall_explanation,
            },

            "recommendation": recommendation,

            "summary": summary,
        }
