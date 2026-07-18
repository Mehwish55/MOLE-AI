import json
import tempfile

from mole_ai.models.registry import (
    create_model_metadata,
    save_model_metadata,
)


def test_create_model_metadata():

    metadata = create_model_metadata(
        "Random Forest",
        "1.0",
        "models/random_forest.pkl",
        {
            "rmse": 0.42,
            "r2": 0.85,
        },
    )

    assert metadata["model_name"] == "Random Forest"
    assert metadata["version"] == "1.0"
    assert metadata["metrics"]["rmse"] == 0.42


def test_save_model_metadata():

    metadata = {
        "model_name": "Test Model",
        "version": "1.0",
    }

    with tempfile.NamedTemporaryFile(
        suffix=".json"
    ) as temp_file:

        save_model_metadata(
            metadata,
            temp_file.name,
        )

        with open(temp_file.name) as file:
            loaded = json.load(file)

        assert loaded["model_name"] == "Test Model"
