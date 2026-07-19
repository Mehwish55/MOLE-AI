from mole_ai.config import get_config


def test_get_config():

    config = get_config()

    assert "dataset" in config

    assert "model" in config

    assert "experiment" in config

    assert config["model"]["test_size"] == 0.2
