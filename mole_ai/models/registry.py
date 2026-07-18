"""
Model registry utilities for MOLE-AI.
"""

import json
from datetime import datetime


def create_model_metadata(
    model_name,
    version,
    model_path,
    metrics=None,
):
    """
    Create model registry metadata.
    """

    metadata = {
        "model_name": model_name,
        "version": version,
        "created": str(datetime.now()),
        "model_path": model_path,
        "metrics": metrics or {},
    }

    return metadata


def save_model_metadata(metadata, output_path):
    """
    Save model metadata as JSON.
    """

    with open(output_path, "w") as file:
        json.dump(
            metadata,
            file,
            indent=4,
        )
