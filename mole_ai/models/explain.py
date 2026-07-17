"""
Model explainability utilities for MOLE-AI.
"""

import pandas as pd


def get_feature_importance(model, feature_names):
    """
    Extract feature importance from tree-based models.

    Parameters
    ----------
    model :
        Trained tree-based model.

    feature_names :
        List of feature names.

    Returns
    -------
    pandas.DataFrame
        Ranked feature importance table.
    """

    importance = model.feature_importances_

    df = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": importance,
        }
    )

    return df.sort_values(
        by="importance",
        ascending=False,
    ).reset_index(drop=True)
