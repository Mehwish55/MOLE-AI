import pandas as pd


"""
Visualization utilities for MOLE-AI.
"""

import matplotlib.pyplot as plt


def plot_activity_distribution(activity, output_path):
    """
    Plot the distribution of activity values.
    """

    plt.figure(figsize=(6, 4))

    plt.hist(activity, bins=10)

    plt.xlabel("Activity")

    plt.ylabel("Count")

    plt.title("Activity Distribution")

    plt.tight_layout()

    plt.savefig(output_path)

    plt.close()


def plot_feature_correlation(df: pd.DataFrame, output_path):
    """
    Plot a feature correlation heatmap.
    """

    plt.figure(figsize=(6, 5))

    correlation = df.corr(numeric_only=True)

    plt.imshow(correlation)

    plt.colorbar()

    plt.xticks(
        range(len(correlation.columns)),
        correlation.columns,
        rotation=90,
    )

    plt.yticks(
        range(len(correlation.columns)),
        correlation.columns,
    )

    plt.tight_layout()

    plt.savefig(output_path)

    plt.close()
