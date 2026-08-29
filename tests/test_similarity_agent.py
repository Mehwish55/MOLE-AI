from mole_ai.agents.similarity_agent import SimilarityAgent


def test_identical_molecules_have_similarity_one():
    agent = SimilarityAgent()

    similarity = agent.calculate_similarity(
        "CCO",
        "CCO",
    )

    assert similarity == 1.0


def test_different_molecules_have_lower_similarity():
    agent = SimilarityAgent()

    similarity = agent.calculate_similarity(
        "CCO",
        "c1ccccc1",
    )

    assert 0.0 <= similarity < 1.0


def test_invalid_smiles_raises_error():
    agent = SimilarityAgent()

    try:
        agent.calculate_similarity(
            "INVALID_SMILES",
            "CCO",
        )
        assert False
    except ValueError:
        assert True


def test_rank_similar_returns_sorted_results():
    agent = SimilarityAgent()

    library = [
        {
            "compound_id": "Compound_001",
            "smiles": "CCO",
        },
        {
            "compound_id": "Compound_002",
            "smiles": "CCN",
        },
        {
            "compound_id": "Compound_003",
            "smiles": "c1ccccc1",
        },
    ]

    results = agent.rank_similar(
        "CCO",
        library,
        top_k=3,
    )

    assert len(results) == 3

    assert results[0]["compound_id"] == "Compound_001"

    similarities = [
        item["similarity"]
        for item in results
    ]

    assert similarities == sorted(
        similarities,
        reverse=True,
    )


def test_top_k_limits_results():
    agent = SimilarityAgent()

    library = [
        {
            "compound_id": "Compound_001",
            "smiles": "CCO",
        },
        {
            "compound_id": "Compound_002",
            "smiles": "CCN",
        },
        {
            "compound_id": "Compound_003",
            "smiles": "c1ccccc1",
        },
    ]

    results = agent.rank_similar(
        "CCO",
        library,
        top_k=2,
    )

    assert len(results) == 2
