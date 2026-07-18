import tempfile

from mole_ai.visualization import plot_activity_distribution


def test_plot_activity_distribution():

    activity = [5.2, 6.1, 7.3, 8.0, 7.8, 6.5]

    with tempfile.NamedTemporaryFile(suffix=".png") as temp_file:

        plot_activity_distribution(
            activity,
            temp_file.name,
        )
