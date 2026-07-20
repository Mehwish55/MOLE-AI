"""
Transformer molecular models for MOLE-AI.
"""

import torch
import torch.nn as nn


class MolecularTransformer(nn.Module):
    """
    Transformer encoder for molecular sequences.
    """

    def __init__(
        self,
        vocab_size,
        embedding_dim=64,
        heads=4,
        layers=2,
    ):
        super().__init__()

        self.embedding = nn.Embedding(
            vocab_size,
            embedding_dim,
        )

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embedding_dim,
            nhead=heads,
            batch_first=True,
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=layers,
        )

        self.output = nn.Linear(
            embedding_dim,
            1,
        )

    def forward(self, tokens):

        x = self.embedding(tokens)

        x = self.transformer(x)

        x = x.mean(dim=1)

        return self.output(x)
