import json
import tempfile

import pandas as pd

from mole_ai.data.metadata import (
    generate_dataset_metadata,
    save_metadata,
)


def test_generate_dataset_metadata():

    df = pd.DataFrame(
        {
            "smiles": ["CCO", "CCC"],
            "activity": [5.2, 6.1],
            "logp": [1.2, 1.5],
        }
    )

    metadata = generate_dataset_metadata(df)

    assert metadata["num_rows"] == 2
    assert metadata["num_columns"] == 3
    assert "smiles" in metadata["columns"]


def test_save_metadata():

    metadata = {
        "num_rows": 10,
        "num_columns": 5,
    }

    with tempfile.NamedTemporaryFile(
        suffix=".json"
    ) as temp_file:

        save_metadata(
            metadata,
            temp_file.name,
        )

        with open(temp_file.name) as file:
            loaded = json.load(file)

        assert loaded["num_rows"] == 10
