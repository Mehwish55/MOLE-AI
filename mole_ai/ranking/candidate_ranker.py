"""
MOLE-AI v2 Multi-Parameter Candidate Ranking.

Combines predicted activity, ADMET performance,
and molecular-property suitability into a transparent
candidate prioritization score.
"""


class CandidateRanker:
    """
    Rank molecules using a transparent multi-parameter
    scoring framework.
    """

    # --------------------------------------------------
    # Main scoring weights
    # --------------------------------------------------

    ACTIVITY_WEIGHT = 0.50
    ADMET_WEIGHT = 0.30
    PROPERTY_WEIGHT = 0.20

    # --------------------------------------------------
    # Activity scoring
    # --------------------------------------------------

    def calculate_activity_score(
        self,
        predicted_pic50: float,
    ) -> float:
        """
        Convert predicted pIC50 into a 0-100 activity score.
        """

        if predicted_pic50 >= 8:
            return 100.0

        elif predicted_pic50 >= 7:
            return 90.0

        elif predicted_pic50 >= 6:
            return 75.0

        elif predicted_pic50 >= 5:
            return 60.0

        else:
            return 40.0

    # --------------------------------------------------
    # Molecular property scoring
    # --------------------------------------------------

    def calculate_property_score(
        self,
        descriptors: dict,
    ) -> float:
        """
        Calculate a molecular-property suitability score.

        This is a transparent heuristic based on common
        drug-likeness ranges. It is not a clinical predictor.
        """

        score = 100.0

        molecular_weight = float(
            descriptors.get("molecular_weight", 0)
        )

        logp = float(
            descriptors.get("logp", 0)
        )

        hbd = float(
            descriptors.get("hbd", 0)
        )

        hba = float(
            descriptors.get("hba", 0)
        )

        tpsa = float(
            descriptors.get("tpsa", 0)
        )

        rotatable_bonds = float(
            descriptors.get("rotatable_bonds", 0)
        )

        # Molecular weight
        if molecular_weight > 500:
            score -= 25
        elif molecular_weight > 450:
            score -= 10

        # LogP
        if logp > 5:
            score -= 20
        elif logp > 4:
            score -= 10

        # Hydrogen bond donors
        if hbd > 5:
            score -= 10

        # Hydrogen bond acceptors
        if hba > 10:
            score -= 10

        # TPSA
        if tpsa > 140:
            score -= 15

        # Rotatable bonds
        if rotatable_bonds > 10:
            score -= 10

        return round(
            max(0.0, min(100.0, score)),
            2,
        )

    # --------------------------------------------------
    # Overall ranking
    # --------------------------------------------------

    def rank(
        self,
        workflow_result: dict,
    ) -> dict:
        """
        Calculate a multi-parameter candidate score.

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
        chemistry = workflow_result["chemistry"]

        predicted_pic50 = float(
            qsar["predicted_pIC50"]
        )

        admet_score = float(
            admet["admet_score"]
        )

        descriptors = chemistry[
            "descriptors"
        ]

        # Calculate individual scores
        activity_score = (
            self.calculate_activity_score(
                predicted_pic50
            )
        )

        property_score = (
            self.calculate_property_score(
                descriptors
            )
        )

        # Transparent weighted score
        overall_score = (
            self.ACTIVITY_WEIGHT * activity_score
            + self.ADMET_WEIGHT * admet_score
            + self.PROPERTY_WEIGHT * property_score
        )

        overall_score = round(
            overall_score,
            2,
        )

        # Candidate priority
        if overall_score >= 80:

            priority = "High Priority"

        elif overall_score >= 60:

            priority = "Medium Priority"

        else:

            priority = "Low Priority"

        return {
            "activity_score": activity_score,
            "admet_score": admet_score,
            "property_score": property_score,
            "overall_score": overall_score,
            "priority": priority,
            "weights": {
                "activity": self.ACTIVITY_WEIGHT,
                "admet": self.ADMET_WEIGHT,
                "molecular_properties": self.PROPERTY_WEIGHT,
            },
        }
