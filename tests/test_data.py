import pandas as pd

from mole_ai.data.downloader import load_csv
from mole_ai.data.validation import validate_columns
from mole_ai.data.preprocessing import (
    remove_missing,
    remove_duplicates
)


def test_load_csv():

    df = load_csv("data/raw/sample.csv")

    assert len(df) > 0
    assert "smiles" in df.columns
    assert "activity" in df.columns



def test_validate_columns():

    df = pd.DataFrame(
        {
            "smiles": ["CCO"],
            "activity": [1]
        }
    )

    assert validate_columns(df) is True



def test_remove_missing():

    df = pd.DataFrame(
        {
            "smiles": ["CCO", None],
            "activity": [1, 0]
        }
    )

    cleaned = remove_missing(df)

    assert len(cleaned) == 1



def test_remove_duplicates():

    df = pd.DataFrame(
        {
            "smiles": ["CCO", "CCO", "CCC"],
            "activity": [1, 1, 0]
        }
    )

    cleaned = remove_duplicates(df)

    assert len(cleaned) == 2
