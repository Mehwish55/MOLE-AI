import numpy as np
import pandas as pd

from mole_ai.models.admet import (
    predict_admet,
    create_admet_profile,
)


class DummyADMETModel:

    def predict(self, features):
        return np.array(
            [
                [0.5],
                [0.8],
            ]
        )


def test_predict_admet():

    model = DummyADMETModel()

    features = pd.DataFrame(
        {
            "feature_1": [1, 2],
        }
    )

    result = predict_admet(
        model,
        features,
    )

    assert isinstance(
        result,
        pd.DataFrame,
    )

    assert "admet_prediction" in result.columns

    assert len(result) == 2


def test_create_admet_profile():

    predictions = {
        "toxicity": 0.1,
        "solubility": 0.8,
        "lipophilicity": 2.5,
        "bbb_permeability": 0.4,
    }

    profile = create_admet_profile(
        predictions,
    )

    assert profile["toxicity"] == 0.1

    assert profile["solubility"] == 0.8

    assert profile["lipophilicity"] == 2.5

    assert profile["bbb_permeability"] == 0.4
