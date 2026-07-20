"""
Docking integration utilities for MOLE-AI.
"""

import pandas as pd


def create_docking_results(
    smiles,
    binding_affinity,
):
    """
    Create a docking results table.

    Parameters
    ----------
    smiles : list
        Molecule SMILES strings.

    binding_affinity : list
        Docking binding affinity values (kcal/mol).

    Returns
    -------
    pandas.DataFrame
        Docking results.
    """

    return pd.DataFrame(
        {
            "smiles": smiles,
            "binding_affinity": binding_affinity,
        }
    )


def rank_docking_results(results):
    """
    Rank docking results.

    Lower binding affinity indicates stronger binding.

    Parameters
    ----------
    results : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
        Ranked docking results.
    """

    return results.sort_values(
        by="binding_affinity",
        ascending=True,
    ).reset_index(drop=True)
