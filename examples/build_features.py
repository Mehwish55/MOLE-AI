from mole_ai.data.downloader import load_csv
from mole_ai.features.builder import build_feature_matrix
from mole_ai.features.export import save_features


def main():

    df = load_csv("data/raw/sample.csv")

    features = build_feature_matrix(df)

    save_features(
        features,
        "data/processed/features.csv"
    )

    print(features.head())
    print("\nFeature matrix saved successfully!")


if __name__ == "__main__":
    main()
