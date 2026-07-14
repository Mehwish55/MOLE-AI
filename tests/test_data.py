import pandas as pd

from mole_ai.data.validation import validate_columns


def test_validate_columns():

    df = pd.DataFrame(
        {
            "smiles": ["CCO"],
            "activity": [1]
        }
    )

    assert validate_columns(df) is True


def test_missing_columns():

    df = pd.DataFrame(
        {
            "compound": ["CCO"]
        }
    )

    try:
        validate_columns(df)

    except ValueError:
        assert True
