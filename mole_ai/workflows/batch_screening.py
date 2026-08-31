"""
MOLE-AI v2 Batch Screening Workflow.

Processes multiple molecules through the complete
drug discovery workflow and returns a ranked table.
"""

import pandas as pd

from mole_ai.workflows.drug_discovery import (
    DrugDiscoveryWorkflow,
)


class BatchScreeningWorkflow:
    """
    Screen multiple molecules using the MOLE-AI pipeline.
    """

    def __init__(self):
        self.workflow = DrugDiscoveryWorkflow()

    def screen(
        self,
        dataframe: pd.DataFrame,
        smiles_column: str = "smiles",
        compound_id_column: str = "compound_id",
    ) -> pd.DataFrame:
        """
        Screen a dataframe of molecules.

        The SMILES column is required.
        The compound ID column is optional.

        Parameters
        ----------
        dataframe : pd.DataFrame
            Input dataframe containing SMILES.

        smiles_column : str
            Name of the SMILES column.

        compound_id_column : str
            Optional name of the compound ID column.

        Returns
        -------
        pd.DataFrame
            Ranked screening results.
        """

        if smiles_column not in dataframe.columns:
            raise ValueError(
                f"Missing required column: {smiles_column}"
            )

        has_compound_id = compound_id_column in dataframe.columns

        results = []

        for index, row in dataframe.iterrows():

            smiles = str(row[smiles_column]).strip()

            if has_compound_id:
                compound_id = str(
                    row[compound_id_column]
                ).strip()

                if not compound_id or compound_id.lower() == "nan":
                    compound_id = f"Molecule_{index + 1:03d}"
            else:
                compound_id = f"Molecule_{index + 1:03d}"

            try:

                result = self.workflow.analyze(smiles)

                # Generated candidate results
                generation = result.get(
                    "generation",
                    []
                )

                evaluated_candidates = result.get(
                    "generated_candidate_evaluation",
                    []
                )

                # Find best evaluated generated candidate
                if evaluated_candidates:
                    best_candidate = max(
                        evaluated_candidates,
                        key=lambda item: item.get(
                            "overall_score",
                            float("-inf"),
                        ),
                    )
                else:
                    best_candidate = {}

                results.append(
                    {
                        "Compound ID": compound_id,
                        "SMILES": smiles,

                        "Molecular Formula":
                            result[
                                "chemistry"
                            ][
                                "descriptors"
                            ][
                                "molecular_formula"
                            ],

                        "Predicted pIC50":
                            result[
                                "qsar"
                            ][
                                "predicted_pIC50"
                            ],

                        "Activity":
                            result[
                                "qsar"
                            ][
                                "activity_class"
                            ],

                        "ADMET Score":
                            result[
                                "admet"
                            ][
                                "admet_score"
                            ],

                        "Overall Score":
                            result[
                                "ranking"
                            ][
                                "overall_score"
                            ],

                        "Priority":
                            result[
                                "ranking"
                            ][
                                "priority"
                            ],

                        # Generated candidate summary
                        "Generated Candidates":
                            len(generation),

                        "Best Generated Score":
                            best_candidate.get(
                                "overall_score"
                            ),

                        "Best Generated pIC50":
                            best_candidate.get(
                                "predicted_pIC50"
                            ),

                        "Best Generated ADMET":
                            best_candidate.get(
                                "admet_score"
                            ),

                        "Best Candidate ID":
                            best_candidate.get(
                                "candidate_id"
                            ),

                        "Best Candidate Similarity":
                            best_candidate.get(
                                "similarity"
                            ),

                        "Best Candidate Priority":
                            best_candidate.get(
                                "priority"
                            ),

                        "Status":
                            "Success",
                    }
                )
            except Exception as error:

                results.append(
                    {
                        "Compound ID": compound_id,
                        "SMILES": smiles,
                        "Molecular Formula": None,
                        "Predicted pIC50": None,
                        "Activity": None,
                        "ADMET Score": None,
                        "Overall Score": None,
                        "Priority": None,

                        "Generated Candidates": 0,
                        "Best Generated Score": None,
                        "Best Generated pIC50": None,
                        "Best Generated ADMET": None,
                        "Best Candidate ID": None,
                        "Best Candidate Similarity": None,
                        "Best Candidate Priority": None,

                        "Status": f"Error: {error}",
                    }
                )

        results_df = pd.DataFrame(results)

        if not results_df.empty:

            results_df = results_df.sort_values(
                by="Overall Score",
                ascending=False,
                na_position="last",
            )

            results_df.insert(
                0,
                "Rank",
                range(1, len(results_df) + 1),
            )

        return results_df
