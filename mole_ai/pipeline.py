"""
End-to-end QSAR pipeline for MOLE-AI.
"""

from mole_ai.models.train import train_models
from mole_ai.models.evaluate import compare_models


def run_qsar_pipeline(
    X,
    y,
):
    """
    Run complete QSAR modelling workflow.

    Parameters
    ----------
    X :
        Feature matrix.

    y :
        Activity values.

    Returns
    -------
    dict
        Trained models and evaluation results.
    """

    models, X_test, y_test = train_models(
        X,
        y,
    )

    results = compare_models(
        models,
        X_test,
        y_test,
    )

    return {
        "models": models,
        "results": results,
    }
