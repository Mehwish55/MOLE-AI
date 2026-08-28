"""
MOLE-AI v2 Export Utilities.
"""

import pandas as pd


def dataframe_to_csv(dataframe: pd.DataFrame) -> str:
    """Convert a DataFrame to CSV text for download."""
    return dataframe.to_csv(index=False)
