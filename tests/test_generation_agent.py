from mole_ai.agents.generation_agent import MolecularGenerationAgent


def test_generation_agent_initializes():
    agent = MolecularGenerationAgent()

    assert agent.radius == 2
    assert agent.n_bits == 2048


def test_generate_candidates_returns_list():
    agent = MolecularGenerationAgent()

    results = agent.generate_candidates("CCO")

    assert isinstance(results, list)


def test_generated_candidates_have_required_fields():
    agent = MolecularGenerationAgent()

    results = agent.generate_candidates("c1ccccc1")

    assert len(results) > 0

    for candidate in results:
        assert "candidate_id" in candidate
        assert "smiles" in candidate
        assert "strategy" in candidate
        assert "similarity" in candidate


def test_generated_smiles_are_valid():
    from rdkit import Chem

    agent = MolecularGenerationAgent()

    results = agent.generate_candidates("c1ccccc1")

    for candidate in results:
        molecule = Chem.MolFromSmiles(candidate["smiles"])

        assert molecule is not None


def test_similarity_is_between_zero_and_one():
    agent = MolecularGenerationAgent()

    results = agent.generate_candidates("c1ccccc1")

    for candidate in results:
        assert 0.0 <= candidate["similarity"] <= 1.0


def test_invalid_parent_smiles_raises_error():
    import pytest

    agent = MolecularGenerationAgent()

    with pytest.raises(ValueError):
        agent.generate_candidates("INVALID_SMILES")


def test_max_candidates_is_respected():
    agent = MolecularGenerationAgent()

    results = agent.generate_candidates(
        "c1ccccc1",
        max_candidates=3,
    )

    assert len(results) <= 3


def test_candidates_are_sorted_by_similarity():
    agent = MolecularGenerationAgent()

    results = agent.generate_candidates("c1ccccc1")

    similarities = [
        candidate["similarity"]
        for candidate in results
    ]

    assert similarities == sorted(
        similarities,
        reverse=True,
    )
