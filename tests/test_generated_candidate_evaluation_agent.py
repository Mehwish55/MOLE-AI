from mole_ai.agents.generated_candidate_evaluation_agent import (
    GeneratedCandidateEvaluationAgent,
)


def test_evaluate_candidate_returns_expected_fields():
    agent = GeneratedCandidateEvaluationAgent()

    candidate = {
        "candidate_id": "GEN_001",
        "smiles": "CCO",
        "strategy": "Canonicalization",
        "similarity": 1.0,
    }

    result = agent.evaluate_candidate(candidate)

    assert result["candidate_id"] == "GEN_001"
    assert result["smiles"] == "CCO"
    assert result["strategy"] == "Canonicalization"
    assert result["similarity"] == 1.0

    assert "predicted_pIC50" in result
    assert "activity_class" in result
    assert "admet_score" in result
    assert "overall_score" in result
    assert "priority" in result


def test_evaluate_candidate_uses_existing_analysis_agents():
    agent = GeneratedCandidateEvaluationAgent()

    candidate = {
        "candidate_id": "GEN_001",
        "smiles": "CCO",
        "strategy": "Canonicalization",
        "similarity": 1.0,
    }

    result = agent.evaluate_candidate(candidate)

    assert result["predicted_pIC50"] == 4.742
    assert result["admet_score"] == 100
    assert result["overall_score"] == 70.0


def test_evaluate_candidates_returns_ranked_results():
    agent = GeneratedCandidateEvaluationAgent()

    candidates = [
        {
            "candidate_id": "GEN_001",
            "smiles": "CCO",
            "strategy": "Canonicalization",
            "similarity": 1.0,
        },
        {
            "candidate_id": "GEN_002",
            "smiles": "CC",
            "strategy": "Test variant",
            "similarity": 0.8,
        },
    ]

    results = agent.evaluate_candidates(candidates)

    assert isinstance(results, list)
    assert len(results) == 2

    assert results[0]["overall_score"] >= results[1]["overall_score"]


def test_invalid_candidate_is_rejected():
    agent = GeneratedCandidateEvaluationAgent()

    candidate = {
        "candidate_id": "GEN_BAD",
        "strategy": "Invalid",
        "similarity": 0.5,
    }

    try:
        agent.evaluate_candidate(candidate)
        assert False, "Expected ValueError"
    except ValueError:
        assert True
