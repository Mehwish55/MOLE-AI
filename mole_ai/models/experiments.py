"""
Experiment tracking utilities for MOLE-AI.
"""

import json
from datetime import datetime


def create_experiment_record(
    experiment_name,
    model_name,
    parameters,
    metrics,
    dataset,
):
    """
    Create an experiment tracking record.
    """

    record = {
        "experiment_name": experiment_name,
        "model_name": model_name,
        "parameters": parameters,
        "metrics": metrics,
        "dataset": dataset,
        "created": str(datetime.now()),
    }

    return record


def save_experiment_record(record, output_path):
    """
    Save experiment record as JSON.
    """

    with open(output_path, "w") as file:
        json.dump(
            record,
            file,
            indent=4,
        )
