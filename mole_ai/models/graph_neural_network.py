"""
Graph neural network utilities for MOLE-AI.
"""

import torch
import torch.nn as nn


class MolecularGraphNetwork(nn.Module):
    """
    Simple graph neural network foundation.
    """

    def __init__(
        self,
        node_features,
        hidden_size=64,
    ):
        super().__init__()

        self.node_encoder = nn.Linear(
            node_features,
            hidden_size,
        )

        self.output = nn.Linear(
            hidden_size,
            1,
        )

    def forward(
        self,
        node_features,
    ):
        """
        Forward pass.

        Parameters
        ----------
        node_features :
            Atom feature tensor.

        Returns
        -------
        torch.Tensor
            Molecular property prediction.
        """

        x = torch.relu(
            self.node_encoder(node_features)
        )

        return self.output(x.mean(dim=0))
