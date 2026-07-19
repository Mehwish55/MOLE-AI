import torch

from mole_ai.models.graph_neural_network import MolecularGraphNetwork


def test_graph_network_forward():

    model = MolecularGraphNetwork(
        node_features=5,
        hidden_size=8,
    )

    node_features = torch.randn(
        6,
        5,
    )

    output = model(node_features)

    assert output.shape == (1,)


def test_graph_network_prediction():

    model = MolecularGraphNetwork(
        node_features=3,
    )

    node_features = torch.tensor(
        [
            [1.0, 0.5, 0.2],
            [0.3, 1.2, 0.8],
            [0.7, 0.1, 1.5],
        ]
    )

    prediction = model(node_features)

    assert prediction.numel() == 1
