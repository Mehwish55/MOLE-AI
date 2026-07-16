"""
Utilities for saving and loading machine learning models.
"""

import joblib


def save_model(model, file_path):
    """
    Save a trained model to disk.
    """
    joblib.dump(model, file_path)


def load_model(file_path):
    """
    Load a trained model from disk.
    """
    return joblib.load(file_path)
