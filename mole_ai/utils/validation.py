"""
MOLE-AI v2 CSV Validation Utilities.
"""

import pandas as pd
from rdkit import Chem


def validate_molecular_library(
    dataframe: pd.DataFrame,
    smiles_column: str = "smiles",
) -> dict:
    """
    Validate a molecular library before batch screening.

    Checks:
    - Required SMILES column
    - Empty SMILES values
    - Valid/invalid SMILES
    - Duplicate SMILES
    """

    result = {
        "valid": False,
        "total_molecules": 0,
        "valid_molecules": 0,
        "invalid_molecules": 0,
        "empty_molecules": 0,
        "duplicate_molecules": 0,
        "invalid_smiles": [],
        "message": "",
    }

    # Check input
    if dataframe is None or dataframe.empty:
        result["message"] = "CSV file is empty."
        return result

    # Check SMILES column
    if smiles_column not in dataframe.columns:
        result["message"] = (
            f"CSV must contain a '{smiles_column}' column."
        )
        return result

    result["total_molecules"] = len(dataframe)

    # Remove missing/empty values for validation
    smiles_series = dataframe[smiles_column].fillna("").astype(str).str.strip()

    empty_mask = smiles_series == ""
    result["empty_molecules"] = int(empty_mask.sum())

    valid_smiles = []
    invalid_smiles = []

    for smiles in smiles_series:
        if not smiles:
            continue

        molecule = Chem.MolFromSmiles(smiles)

        if molecule is None:
            invalid_smiles.append(smiles)
        else:
            valid_smiles.append(smiles)

    result["valid_molecules"] = len(valid_smiles)
    result["invalid_molecules"] = len(invalid_smiles)
    result["invalid_smiles"] = invalid_smiles

    # Count duplicate molecular entries
    non_empty_smiles = smiles_series[~empty_mask]
    result["duplicate_molecules"] = int(
        non_empty_smiles.duplicated().sum()
    )

    # Dataset is ready only when all entries are valid and non-empty
    result["valid"] = (
        result["total_molecules"] > 0
        and result["invalid_molecules"] == 0
        and result["empty_molecules"] == 0
    )

    if result["valid"]:
        result["message"] = (
            "CSV validation successful. "
            "The molecular library is ready for screening."
        )
    else:
        result["message"] = (
            "CSV validation found issues. "
            "Please review the dataset before screening."
        )

    return result
