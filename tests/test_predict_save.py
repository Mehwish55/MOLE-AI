import pandas as pd

from mole_ai.models.predict import save_predictions


def test_save_predictions(tmp_path):

    predictions = pd.Series(
        [7.2, 6.8, 8.1],
        name="predicted_pIC50",
    )

    output = tmp_path / "predictions.csv"

    save_predictions(predictions, output)

    loaded = pd.read_csv(output)

    assert len(loaded) == 3
    assert "predicted_pIC50" in loaded.columns
