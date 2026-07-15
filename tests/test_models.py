import pandas as pd

from mole_ai.models.train import load_feature_dataset


def test_load_feature_dataset(tmp_path):

    sample = tmp_path / "features.csv"

    df = pd.DataFrame(
        {
            "feature1": [1, 2],
            "activity": [7.1, 6.8]
        }
    )

    df.to_csv(sample, index=False)

    loaded = load_feature_dataset(sample)

    assert len(loaded) == 2
    assert "activity" in loaded.columns
