"""
MOLE-AI v2 Candidate Comparison and Visualization Utilities.

Provides summary statistics, candidate selection, priority
distribution, and recommendations for screened molecular libraries.
"""

import pandas as pd


class CandidateComparison:
    """
    Analyze and compare ranked molecular screening results.
    """

    REQUIRED_COLUMNS = [
        "SMILES",
        "Predicted pIC50",
        "Activity",
        "ADMET Score",
        "Overall Score",
        "Priority",
        "Status",
    ]

    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe.copy()

        self._validate_dataframe()

    # ============================================================
    # Validation
    # ============================================================

    def _validate_dataframe(self):
        """Validate the screening results dataframe."""

        missing = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in self.dataframe.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

    # ============================================================
    # Successful Results
    # ============================================================

    def successful_results(self) -> pd.DataFrame:
        """Return successfully analyzed molecules."""

        return self.dataframe[
            self.dataframe["Status"] == "Success"
        ].copy()

    # ============================================================
    # Summary
    # ============================================================

    def summary(self) -> dict:
        """Generate screening summary statistics."""

        total = len(self.dataframe)

        successful_df = self.successful_results()

        successful = len(successful_df)

        success_rate = (
            (successful / total) * 100
            if total > 0
            else 0.0
        )

        high_priority = len(
            successful_df[
                successful_df["Priority"]
                == "High Priority"
            ]
        )

        medium_priority = len(
            successful_df[
                successful_df["Priority"]
                == "Medium Priority"
            ]
        )

        low_priority = len(
            successful_df[
                successful_df["Priority"]
                == "Low Priority"
            ]
        )

        return {
            "total_molecules": total,
            "successful_molecules": successful,
            "success_rate": round(
                success_rate,
                1,
            ),
            "high_priority_count": high_priority,
            "medium_priority_count": medium_priority,
            "low_priority_count": low_priority,
        }

    # ============================================================
    # Top Candidate
    # ============================================================

    def top_candidate(self):
        """
        Return the candidate with the highest overall score.
        """

        successful_df = self.successful_results()

        if successful_df.empty:
            return None

        row = successful_df.sort_values(
            "Overall Score",
            ascending=False,
        ).iloc[0]

        return {
            "smiles": row["SMILES"],
            "predicted_pIC50": float(
                row["Predicted pIC50"]
            ),
            "activity": row["Activity"],
            "admet_score": float(
                row["ADMET Score"]
            ),
            "overall_score": float(
                row["Overall Score"]
            ),
            "priority": row["Priority"],
        }

    # ============================================================
    # Best Activity Candidate
    # ============================================================

    def best_activity_candidate(self):
        """
        Return the candidate with the highest predicted pIC50.
        """

        successful_df = self.successful_results()

        if successful_df.empty:
            return None

        row = successful_df.sort_values(
            "Predicted pIC50",
            ascending=False,
        ).iloc[0]

        return {
            "smiles": row["SMILES"],
            "predicted_pIC50": float(
                row["Predicted pIC50"]
            ),
            "activity": row["Activity"],
        }

    # ============================================================
    # Top Candidates
    # ============================================================

    def top_candidates(
        self,
        n: int = 5,
    ) -> pd.DataFrame:
        """
        Return the top N candidates ranked by overall score.
        """

        successful_df = self.successful_results()

        if successful_df.empty:
            return successful_df

        return (
            successful_df
            .sort_values(
                "Overall Score",
                ascending=False,
            )
            .head(n)
            .reset_index(drop=True)
        )

    # ============================================================
    # Priority Distribution
    # ============================================================

    def priority_distribution(self) -> pd.Series:
        """Return counts for each candidate priority."""

        successful_df = self.successful_results()

        return (
            successful_df["Priority"]
            .value_counts()
            .reindex(
                [
                    "High Priority",
                    "Medium Priority",
                    "Low Priority",
                ],
                fill_value=0,
            )
        )

    # ============================================================
    # Activity Distribution
    # ============================================================

    def activity_distribution(self) -> pd.Series:
        """Return counts for activity classifications."""

        successful_df = self.successful_results()

        return successful_df[
            "Activity"
        ].value_counts()

    # ============================================================
    # Ranking Table
    # ============================================================

    def ranking_table(self) -> pd.DataFrame:
        """
        Return a clean candidate comparison table.
        """

        successful_df = self.successful_results()

        if successful_df.empty:
            return successful_df

        columns = [
            "Rank",
            "SMILES",
            "Predicted pIC50",
            "Activity",
            "ADMET Score",
            "Overall Score",
            "Priority",
        ]

        available_columns = [
            column
            for column in columns
            if column in successful_df.columns
        ]

        return (
            successful_df[
                available_columns
            ]
            .sort_values(
                "Overall Score",
                ascending=False,
            )
            .reset_index(drop=True)
        )

    # ============================================================
    # Recommendation
    # ============================================================

    def recommendation(self) -> str:
        """
        Generate a simple scientific screening recommendation.
        """

        successful_df = self.successful_results()

        if successful_df.empty:

            return (
                "No molecules were successfully analyzed. "
                "Review the input SMILES and screening errors."
            )

        high_priority = len(
            successful_df[
                successful_df["Priority"]
                == "High Priority"
            ]
        )

        top = self.top_candidate()

        if high_priority > 0:

            return (
                f"{high_priority} high-priority candidate(s) "
                "were identified. These molecules should be "
                "considered first for further computational "
                "validation."
            )

        if top is not None:

            return (
                "No high-priority candidates were identified. "
                "The highest-ranked molecule may still be "
                "considered for further optimization and "
                "computational validation."
            )

        return (
            "Further molecular optimization and validation "
            "are recommended."
        )

    # ============================================================
    # Complete Analysis
    # ============================================================

    def analyze(self) -> dict:
        """
        Generate complete candidate comparison analysis.
        """

        return {
            "summary": self.summary(),
            "top_candidate": self.top_candidate(),
            "best_activity_candidate": (
                self.best_activity_candidate()
            ),
            "top_candidates": self.top_candidates(
                5
            ),
            "priority_distribution": (
                self.priority_distribution()
            ),
            "activity_distribution": (
                self.activity_distribution()
            ),
            "recommendation": self.recommendation(),
        }
