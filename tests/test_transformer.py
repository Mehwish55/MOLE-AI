import torch

from mole_ai.models.transformer import MolecularTransformer


def test_transformer_forward():

    model = MolecularTransformer(
        vocab_size=20,
        embedding_dim=32,
        heads=4,
        layers=1,
    )

    tokens = torch.randint(
        0,
        20,
        (2, 10),
    )

    output = model(tokens)

    assert output.shape == (2, 1)


def test_transformer_single_sequence():

    model = MolecularTransformer(
        vocab_size=10,
    )

    tokens = torch.tensor(
        [
            [1, 2, 3, 4, 5]
        ]
    )

    prediction = model(tokens)

    assert prediction.numel() == 1
