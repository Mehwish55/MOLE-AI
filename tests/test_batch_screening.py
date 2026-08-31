import pandas as pd

from mole_ai.workflows.batch_screening import (
    BatchScreeningWorkflow,
)


def test_batch_screening_returns_expected_columns():
    dataframe = pd.DataFrame(
        {
            "compound_id": ["CMP_001"],
            "smiles": ["CCO"],
        }
    )

    workflow = BatchScreeningWorkflow()

    results = workflow.screen(dataframe)

    assert len(results) == 1

    expected_columns = [
        "Rank",
        "Compound ID",
        "SMILES",
        "Molecular Formula",
        "Predicted pIC50",
        "Activity",
        "ADMET Score",
        "Overall Score",
        "Priority",
        "Generated Candidates",
        "Best Generated Score",
        "Best Generated pIC50",
        "Best Generated ADMET",
        "Best Candidate ID",
        "Best Candidate Similarity",
        "Best Candidate Priority",
        "Status",
    ]

    for column in expected_columns:
        assert column in results.columns


def test_batch_screening_includes_generated_candidate_summary():
    dataframe = pd.DataFrame(
        {
            "compound_id": ["CMP_001"],
            "smiles": ["CCO"],
        }
    )

    workflow = BatchScreeningWorkflow()

    results = workflow.screen(dataframe)

    row = results.iloc[0]

    assert row["Status"] == "Success"
    assert row["Generated Candidates"] > 0
    assert row["Best Candidate ID"] is not None
    assert row["Best Generated Score"] is not None


def test_batch_screening_handles_multiple_molecules():
    dataframe = pd.DataFrame(
        {
            "compound_id": [
                "CMP_001",
                "CMP_002",
            ],
            "smiles": [
                "CCO",
                "CCN",
            ],
        }
    )

    workflow = BatchScreeningWorkflow()

    results = workflow.screen(dataframe)

    assert len(results) == 2
    assert all(
        results["Generated Candidates"] > 0
    )
