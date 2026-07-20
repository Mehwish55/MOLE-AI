import pandas as pd

from mole_ai.pipeline import run_qsar_pipeline


def test_run_qsar_pipeline():

    X = pd.DataFrame(
        {
            "feature_1": [1, 2, 3, 4, 5, 6],
            "feature_2": [5, 4, 3, 2, 1, 0],
        }
    )

    y = pd.Series(
        [1.1, 2.2, 3.0, 4.1, 5.2, 6.0]
    )

    result = run_qsar_pipeline(
        X,
        y,
    )

    assert "models" in result

    assert "results" in result

    assert len(result["models"]) > 0

    assert len(result["results"]) > 0
