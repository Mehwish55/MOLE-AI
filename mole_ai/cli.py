"""
Command-line interface for MOLE-AI.
"""

import argparse
import pandas as pd

from mole_ai.models.utils import load_model
from mole_ai.models.predict import predict_from_dataframe


def main():

    parser = argparse.ArgumentParser(
        description="MOLE-AI Command Line Interface"
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show MOLE-AI version",
    )

    parser.add_argument(
        "--predict",
        action="store_true",
        help="Predict pIC50 values",
    )

    parser.add_argument(
        "--model",
        help="Path to trained model file",
    )

    parser.add_argument(
        "--input",
        help="Input CSV feature file",
    )

    parser.add_argument(
        "--output",
        help="Output prediction CSV file",
    )

    args = parser.parse_args()

    if args.version:
        print("MOLE-AI Version 1.0")

    elif args.predict:

        model = load_model(args.model)

        features = pd.read_csv(args.input)

        predictions = predict_from_dataframe(
            model,
            features,
        )

        predictions.to_csv(
            args.output,
            index=False,
        )

        print("Prediction completed successfully")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
