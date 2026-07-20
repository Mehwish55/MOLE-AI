"""
Molecular optimization utilities for MOLE-AI.
"""

import pandas as pd


def rank_candidates(
    candidates: pd.DataFrame,
    activity_weight=0.7,
    admet_weight=0.3,
):
    """
    Rank molecular candidates using weighted activity and ADMET scores.

    Parameters
    ----------
    candidates : pandas.DataFrame
        Must contain 'predicted_pIC50' and 'admet_prediction' columns.

    activity_weight : float
        Weight assigned to predicted activity.

    admet_weight : float
        Weight assigned to ADMET score.

    Returns
    -------
    pandas.DataFrame
        Ranked candidate molecules.
    """

    result = candidates.copy()

    result["optimization_score"] = (
        activity_weight * result["predicted_pIC50"]
        + admet_weight * result["admet_prediction"]
    )

    return result.sort_values(
        by="optimization_score",
        ascending=False,
    ).reset_index(drop=True)
