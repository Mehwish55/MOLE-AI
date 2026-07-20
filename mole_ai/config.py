"""
Configuration management utilities for MOLE-AI.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


CONFIG = {
    "dataset": {
        "raw_path": PROJECT_ROOT / "data" / "raw",
        "processed_path": PROJECT_ROOT / "data" / "processed",
    },

    "model": {
        "random_forest": {
            "n_estimators": 100,
            "random_state": 42,
        },
        "test_size": 0.2,
    },

    "experiment": {
        "name": "MOLE-AI-QSAR",
        "version": "1.0",
    },
}


def get_config():
    """
    Return MOLE-AI configuration.

    Returns
    -------
    dict
        Project configuration.
    """

    return CONFIG
