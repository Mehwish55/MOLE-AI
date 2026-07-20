import json
import tempfile

from mole_ai.models.experiments import (
    create_experiment_record,
    save_experiment_record,
)


def test_create_experiment_record():

    record = create_experiment_record(
        "QSAR experiment 1",
        "Random Forest",
        {
            "n_estimators": 100,
        },
        {
            "rmse": 0.42,
            "r2": 0.85,
        },
        "ChEMBL dataset",
    )

    assert record["experiment_name"] == "QSAR experiment 1"
    assert record["model_name"] == "Random Forest"
    assert record["metrics"]["rmse"] == 0.42
    assert record["dataset"] == "ChEMBL dataset"


def test_save_experiment_record():

    record = {
        "experiment_name": "test",
        "model_name": "model",
    }

    with tempfile.NamedTemporaryFile(
        suffix=".json"
    ) as temp_file:

        save_experiment_record(
            record,
            temp_file.name,
        )

        with open(temp_file.name) as file:
            loaded = json.load(file)

        assert loaded["experiment_name"] == "test"
