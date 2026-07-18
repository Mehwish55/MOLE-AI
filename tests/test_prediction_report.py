import pandas as pd

from mole_ai.models.predict import generate_prediction_report


def test_generate_prediction_report():

    predictions = pd.Series(
        [7.2, 6.8, 8.1],
        name="predicted_pIC50",
    )

    report = generate_prediction_report(
        predictions,
        "Random Forest",
    )

    assert len(report) == 3
    assert "prediction" in report.columns
    assert "model" in report.columns
    assert report["model"].iloc[0] == "Random Forest"
