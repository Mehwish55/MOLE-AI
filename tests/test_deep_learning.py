import torch

from mole_ai.models.deep_learning import QSARNeuralNetwork


def test_qsar_neural_network():

    model = QSARNeuralNetwork(
        input_size=5,
        hidden_size=10,
    )

    X = torch.randn(
        3,
        5,
    )

    output = model(X)

    assert output.shape == (3, 1)


def test_model_forward_pass():

    model = QSARNeuralNetwork(
        input_size=3,
    )

    sample = torch.tensor(
        [
            [1.0, 2.0, 3.0]
        ]
    )

    prediction = model(sample)

    assert prediction.shape == (1, 1)
