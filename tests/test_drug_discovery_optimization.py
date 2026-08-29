from mole_ai.workflows.drug_discovery import DrugDiscoveryWorkflow


def test_drug_discovery_workflow_includes_optimization():
    workflow = DrugDiscoveryWorkflow()

    result = workflow.analyze("CCO")

    assert "optimization" in result

    optimization = result["optimization"]

    assert isinstance(optimization, dict)
    assert "optimization_priority" in optimization
    assert "suggestions" in optimization
    assert "predicted_pIC50" in optimization
    assert "admet_score" in optimization
    assert "overall_score" in optimization
    assert "properties" in optimization


def test_optimization_uses_workflow_results():
    workflow = DrugDiscoveryWorkflow()

    result = workflow.analyze("CCO")

    optimization = result["optimization"]

    assert optimization["predicted_pIC50"] == result["qsar"]["predicted_pIC50"]
    assert optimization["admet_score"] == result["admet"]["admet_score"]
    assert optimization["overall_score"] == result["ranking"]["overall_score"]


def test_complete_workflow_contains_all_major_components():
    workflow = DrugDiscoveryWorkflow()

    result = workflow.analyze("CCO")

    assert "chemistry" in result
    assert "qsar" in result
    assert "admet" in result
    assert "ranking" in result
    assert "optimization" in result


def test_drug_discovery_workflow_includes_generation():
    workflow = DrugDiscoveryWorkflow()

    result = workflow.analyze("CCO")

    assert "generation" in result

    generation = result["generation"]

    assert isinstance(generation, list)
    assert len(generation) > 0

    candidate = generation[0]

    assert isinstance(candidate, dict)
    assert "candidate_id" in candidate
    assert "smiles" in candidate
    assert "strategy" in candidate
    assert "similarity" in candidate


def test_generation_candidates_are_ranked_by_similarity():
    workflow = DrugDiscoveryWorkflow()

    result = workflow.analyze("CCO")

    generation = result["generation"]

    similarities = [
        candidate["similarity"]
        for candidate in generation
    ]

    assert similarities == sorted(
        similarities,
        reverse=True,
    )
