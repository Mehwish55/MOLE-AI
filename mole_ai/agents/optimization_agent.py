"""
MOLE-AI v2 Molecular Optimization Agent.

Provides transparent, rule-based optimization suggestions
based on molecular properties, predicted activity, ADMET,
and candidate ranking.
"""


class MolecularOptimizationAgent:
    """
    Generates interpretable molecular optimization suggestions.

    This agent does not generate new molecules. It identifies
    properties that may be worth optimizing and provides
    transparent recommendations.
    """

    def analyze(
        self,
        workflow_result: dict,
    ) -> dict:
        """
        Analyze a molecule and generate optimization suggestions.
        """

        chemistry = workflow_result.get("chemistry", {})
        qsar = workflow_result.get("qsar", {})
        admet = workflow_result.get("admet", {})
        ranking = workflow_result.get("ranking", {})

        descriptors = chemistry.get("descriptors", {})

        suggestions = []
        priorities = []

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

        predicted_pic50 = float(
            qsar.get("predicted_pIC50", 0)
        )

        admet_score = float(
            admet.get("admet_score", 0)
        )

        overall_score = float(
            ranking.get("overall_score", 0)
        )

        # --------------------------------------------------
        # Molecular weight
        # --------------------------------------------------

        if molecular_weight > 500:
            suggestions.append(
                "Consider reducing molecular weight while preserving "
                "the key molecular scaffold."
            )
            priorities.append("High")

        elif molecular_weight > 450:
            suggestions.append(
                "Molecular weight is relatively high. Consider "
                "modest molecular simplification."
            )
            priorities.append("Medium")

        # --------------------------------------------------
        # LogP
        # --------------------------------------------------

        if logp > 5:
            suggestions.append(
                "High lipophilicity detected. Consider reducing LogP "
                "to potentially improve physicochemical and ADMET "
                "properties."
            )
            priorities.append("High")

        elif logp > 4:
            suggestions.append(
                "LogP is relatively high. Consider structural changes "
                "that modestly reduce lipophilicity."
            )
            priorities.append("Medium")

        # --------------------------------------------------
        # Hydrogen bond donors
        # --------------------------------------------------

        if hbd > 5:
            suggestions.append(
                "Hydrogen bond donor count is elevated. Consider "
                "reducing unnecessary donor groups."
            )
            priorities.append("Medium")

        # --------------------------------------------------
        # Hydrogen bond acceptors
        # --------------------------------------------------

        if hba > 10:
            suggestions.append(
                "Hydrogen bond acceptor count is elevated. Consider "
                "simplifying polar functionality."
            )
            priorities.append("Medium")

        # --------------------------------------------------
        # TPSA
        # --------------------------------------------------

        if tpsa > 140:
            suggestions.append(
                "TPSA is high. Consider reducing excessive polarity "
                "if compatible with the intended target."
            )
            priorities.append("Medium")

        # --------------------------------------------------
        # Rotatable bonds
        # --------------------------------------------------

        if rotatable_bonds > 10:
            suggestions.append(
                "The molecule has many rotatable bonds. Consider "
                "rigidification or scaffold simplification."
            )
            priorities.append("Medium")

        # --------------------------------------------------
        # Activity
        # --------------------------------------------------

        if predicted_pic50 < 5:
            suggestions.append(
                "Predicted activity is relatively low. Structural "
                "optimization should prioritize improving target "
                "activity while preserving acceptable properties."
            )
            priorities.append("High")

        elif predicted_pic50 < 6:
            suggestions.append(
                "Predicted activity is moderate. Consider activity-"
                "focused structural optimization."
            )
            priorities.append("Medium")

        # --------------------------------------------------
        # ADMET
        # --------------------------------------------------

        if admet_score < 60:
            suggestions.append(
                "ADMET score is relatively low. Prioritize improving "
                "drug-like and ADMET-related properties."
            )
            priorities.append("High")

        elif admet_score < 80:
            suggestions.append(
                "ADMET properties have room for improvement."
            )
            priorities.append("Medium")

        # --------------------------------------------------
        # Overall assessment
        # --------------------------------------------------

        if not suggestions:
            suggestions.append(
                "No major optimization liabilities were identified "
                "by the current rule-based assessment."
            )
            priorities.append("Low")

        if "High" in priorities:
            optimization_priority = "High"
        elif "Medium" in priorities:
            optimization_priority = "Medium"
        else:
            optimization_priority = "Low"

        return {
            "optimization_priority": optimization_priority,
            "suggestions": suggestions,
            "predicted_pIC50": predicted_pic50,
            "admet_score": admet_score,
            "overall_score": overall_score,
            "properties": {
                "molecular_weight": molecular_weight,
                "logp": logp,
                "hbd": hbd,
                "hba": hba,
                "tpsa": tpsa,
                "rotatable_bonds": rotatable_bonds,
            },
        }
