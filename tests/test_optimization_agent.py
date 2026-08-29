from mole_ai.agents.optimization_agent import MolecularOptimizationAgent


def test_optimization_agent_returns_expected_structure():
    agent = MolecularOptimizationAgent()

    workflow_result = {
        "chemistry": {
            "descriptors": {
                "molecular_weight": 300,
                "logp": 2.5,
                "hbd": 2,
                "hba": 5,
                "tpsa": 70,
                "rotatable_bonds": 4,
            }
        },
        "qsar": {
            "predicted_pIC50": 7.2,
        },
        "admet": {
            "admet_score": 90,
        },
        "ranking": {
            "overall_score": 85,
        },
    }

    result = agent.analyze(workflow_result)

    assert "optimization_priority" in result
    assert "suggestions" in result
    assert "predicted_pIC50" in result
    assert "admet_score" in result
    assert "overall_score" in result
    assert "properties" in result

    assert result["predicted_pIC50"] == 7.2
    assert result["admet_score"] == 90
    assert result["overall_score"] == 85


def test_high_molecular_weight_generates_warning():
    agent = MolecularOptimizationAgent()

    workflow_result = {
        "chemistry": {
            "descriptors": {
                "molecular_weight": 600,
                "logp": 2,
                "hbd": 2,
                "hba": 5,
                "tpsa": 70,
                "rotatable_bonds": 4,
            }
        },
        "qsar": {
            "predicted_pIC50": 7,
        },
        "admet": {
            "admet_score": 90,
        },
        "ranking": {
            "overall_score": 80,
        },
    }

    result = agent.analyze(workflow_result)

    assert result["optimization_priority"] == "High"
    assert any(
        "molecular weight" in suggestion.lower()
        for suggestion in result["suggestions"]
    )


def test_high_logp_generates_warning():
    agent = MolecularOptimizationAgent()

    workflow_result = {
        "chemistry": {
            "descriptors": {
                "molecular_weight": 300,
                "logp": 6,
                "hbd": 2,
                "hba": 5,
                "tpsa": 70,
                "rotatable_bonds": 4,
            }
        },
        "qsar": {
            "predicted_pIC50": 7,
        },
        "admet": {
            "admet_score": 90,
        },
        "ranking": {
            "overall_score": 80,
        },
    }

    result = agent.analyze(workflow_result)

    assert result["optimization_priority"] == "High"
    assert any(
        "lipophilicity" in suggestion.lower()
        for suggestion in result["suggestions"]
    )


def test_low_activity_generates_activity_suggestion():
    agent = MolecularOptimizationAgent()

    workflow_result = {
        "chemistry": {
            "descriptors": {
                "molecular_weight": 300,
                "logp": 2,
                "hbd": 2,
                "hba": 5,
                "tpsa": 70,
                "rotatable_bonds": 4,
            }
        },
        "qsar": {
            "predicted_pIC50": 4.2,
        },
        "admet": {
            "admet_score": 90,
        },
        "ranking": {
            "overall_score": 60,
        },
    }

    result = agent.analyze(workflow_result)

    assert result["optimization_priority"] == "High"
    assert any(
        "activity" in suggestion.lower()
        for suggestion in result["suggestions"]
    )


def test_good_molecule_has_low_optimization_priority():
    agent = MolecularOptimizationAgent()

    workflow_result = {
        "chemistry": {
            "descriptors": {
                "molecular_weight": 300,
                "logp": 2,
                "hbd": 2,
                "hba": 5,
                "tpsa": 70,
                "rotatable_bonds": 4,
            }
        },
        "qsar": {
            "predicted_pIC50": 8,
        },
        "admet": {
            "admet_score": 95,
        },
        "ranking": {
            "overall_score": 90,
        },
    }

    result = agent.analyze(workflow_result)

    assert result["optimization_priority"] == "Low"
    assert len(result["suggestions"]) >= 1
