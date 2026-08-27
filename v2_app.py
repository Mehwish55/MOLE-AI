"""
MOLE-AI v2
AI-Powered Computational Drug Discovery Platform
"""

import streamlit as st
import pandas as pd

from mole_ai.workflows.drug_discovery import DrugDiscoveryWorkflow
from mole_ai.workflows.batch_screening import BatchScreeningWorkflow
from mole_ai.ranking.explanation import CandidateExplainer

# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="MOLE-AI v2",
    page_icon="🧬",
    layout="wide",
)


# ============================================================
# Header
# ============================================================

st.title("🧬 MOLE-AI v2")

st.markdown(
    """
    ### AI-Powered Computational Drug Discovery Platform

    Integrating **cheminformatics, machine learning,
    molecular property analysis, ADMET screening,
    and candidate prioritization**.
    """
)

st.divider()


# ============================================================
# Navigation
# ============================================================

tab1, tab2 = st.tabs(
    [
        "🔬 Single Molecule Analysis",
        "📂 Batch Screening",
    ]
)


# ============================================================
# TAB 1 — SINGLE MOLECULE ANALYSIS
# ============================================================

with tab1:

    st.header("🔬 Single Molecule Analysis")

    smiles = st.text_input(
        "Enter molecular SMILES",
        placeholder="Example: CCO",
    )

    analyze_button = st.button(
        "🚀 Analyze Molecule",
        type="primary",
    )

    if analyze_button:

        if not smiles.strip():

            st.warning(
                "Please enter a SMILES string."
            )

        else:

            try:

                with st.spinner(
                    "Running MOLE-AI v2 analysis..."
                ):

                    workflow = DrugDiscoveryWorkflow()

                    result = workflow.analyze(
                        smiles.strip()
                    )
                    explainer = CandidateExplainer()

                    explanation = explainer.explain(result)

                st.success(
                    "✅ Molecular analysis completed"
                )

                # ====================================================
                # Extract Results
                # ====================================================

                ranking = result["ranking"]
                qsar = result["qsar"]
                admet = result["admet"]
                chemistry = result["chemistry"]

                descriptors = chemistry["descriptors"]


                # ====================================================
                # Candidate Assessment
                # ====================================================

                st.subheader(
                    "🎯 Candidate Assessment"
                )

                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.metric(
                        "Overall Score",
                        f"{ranking['overall_score']:.1f}",
                    )

                with col2:

                    st.metric(
                        "Predicted pIC50",
                        f"{qsar['predicted_pIC50']:.3f}",
                    )

                with col3:

                    st.metric(
                        "ADMET Score",
                        f"{admet['admet_score']:.1f}",
                    )

                with col4:

                    st.metric(
                        "Priority",
                        ranking["priority"],
                    )


                # ====================================================
                # Candidate Score Profile
                # ====================================================

                st.markdown(
                    "### 📊 Candidate Score Profile"
                )

                score_df = pd.DataFrame(
                    {
                        "Score": [
                            float(
                                ranking["activity_score"]
                            ),
                            float(
                                ranking["admet_score"]
                            ),
                            float(
                                ranking["overall_score"]
                            ),
                        ]
                    },
                    index=[
                        "Activity",
                        "ADMET",
                        "Overall",
                    ],
                )

                st.bar_chart(
                    score_df,
                    y="Score",
                    width="stretch",
                )


                st.divider()

                # ====================================================
                # Chemistry Analysis
                # ====================================================

                st.subheader(
                    "🧪 Chemistry Analysis"
                )

                chemistry_df = pd.DataFrame(
                    list(descriptors.items()),
                    columns=[
                        "Property",
                        "Value",
                    ],
                )

                # Convert values to strings to avoid
                # mixed-type Arrow serialization problems.
                chemistry_df["Value"] = (
                    chemistry_df["Value"].astype(str)
                )

                st.dataframe(
                    chemistry_df,
                    width="stretch",
                    hide_index=True,
                )


                st.divider()


                # ====================================================
                # QSAR Prediction
                # ====================================================

                st.subheader(
                    "🤖 QSAR Prediction"
                )

                qsar_col1, qsar_col2 = st.columns(2)

                with qsar_col1:

                    st.metric(
                        "Predicted pIC50",
                        f"{qsar['predicted_pIC50']:.3f}",
                    )

                with qsar_col2:

                    st.metric(
                        "Activity Classification",
                        qsar["activity_class"],
                    )

                st.info(
                    f"Model: {qsar['model']}"
                )


                st.divider()


                # ====================================================
                # ADMET Analysis
                # ====================================================

                st.subheader(
                    "💊 ADMET / Drug-Likeness"
                )

                admet_col1, admet_col2 = st.columns(2)

                with admet_col1:

                    st.metric(
                        "ADMET Score",
                        f"{admet['admet_score']:.1f}",
                    )

                with admet_col2:

                    st.write(
                        "Drug-likeness"
                    )

                    if (
                        "Drug-like"
                        in admet["drug_likeness"]
                    ):

                        st.success(
                            admet["drug_likeness"]
                        )

                    else:

                        st.warning(
                            admet["drug_likeness"]
                        )


                # ADMET properties
                if "properties" in admet:

                    st.markdown(
                        "### ADMET Properties"
                    )

                    admet_df = pd.DataFrame(
                        list(
                            admet[
                                "properties"
                            ].items()
                        ),
                        columns=[
                            "Property",
                            "Value",
                        ],
                    )

                    admet_df["Value"] = (
                        admet_df["Value"].astype(str)
                    )

                    st.dataframe(
                        admet_df,
                        width="stretch",
                        hide_index=True,
                    )


                st.divider()


                # ====================================================
                # Candidate Ranking
                # ====================================================

                st.subheader(
                    "🎯 Candidate Prioritization"
                )


                # Three aligned numerical metrics
                rank_col1, rank_col2, rank_col3 = st.columns(3)

                with rank_col1:

                    st.metric(
                        "Activity Score",
                        f"{ranking['activity_score']:.1f}",
                    )

                with rank_col2:

                    st.metric(
                        "ADMET Score",
                        f"{ranking['admet_score']:.1f}",
                    )

                with rank_col3:

                    st.metric(
                        "Overall Score",
                        f"{ranking['overall_score']:.1f}",
                    )


                st.write("")


                # ====================================================
                # Priority Indicator
                # ====================================================

                st.markdown(
                    "### 🏆 Candidate Priority"
                )

                priority = ranking["priority"]

                if priority == "High Priority":

                    st.success(
                        f"🟢 **{priority}**"
                    )

                elif priority == "Medium Priority":

                    st.warning(
                        f"🟡 **{priority}**"
                    )

                else:

                    st.info(
                        f"🔵 **{priority}**"
                    )


                # ====================================================
                # Ranking Summary
                # ====================================================

                st.markdown(
                    "### 📊 Ranking Summary"
                )

                ranking_df = pd.DataFrame(
                    {
                        "Metric": [
                            "Activity Score",
                            "ADMET Score",
                            "Overall Score",
                        ],
                        "Score": [
                            float(
                                ranking[
                                    "activity_score"
                                ]
                            ),
                            float(
                                ranking[
                                    "admet_score"
                                ]
                            ),
                            float(
                                ranking[
                                    "overall_score"
                                ]
                            ),
                        ],
                    }
                )

                st.dataframe(
                    ranking_df,
                    width="stretch",
                    hide_index=True,
                )


                # ====================================================
                # Ranking Interpretation
                # ====================================================

                st.markdown(
                    "### 🧠 Ranking Interpretation"
                )

                st.write(
                    f"""
                    **Activity Score:** \
{ranking['activity_score']:.1f}/100

                    **ADMET Score:** \
{ranking['admet_score']:.1f}/100

                    **Overall Score:** \
{ranking['overall_score']:.1f}/100

                    **Final Priority:** \
{ranking['priority']}
                    """
                )


                st.divider()
                # ====================================================
                # AI Candidate Explainability
                # ====================================================
                
                st.subheader(
                    "🧠 AI Candidate Explainability"
                )
                
                st.markdown(
                    "### 🔬 Activity Interpretation"
                )
                
                st.info(
                    explanation["activity"]["interpretation"]
                )
                
                st.write(
                    f"**Predicted pIC50:** "
                    f"{explanation['activity']['predicted_pIC50']:.3f}"
                )
                
                st.write(
                    f"**Activity Classification:** "
                    f"{explanation['activity']['classification']}"
                )
                
                st.write(
                    f"**Activity Score:** "
                    f"{explanation['activity']['score']:.1f}/100"
                )
                
                
                st.markdown(
                    "### 💊 ADMET Interpretation"
                )
                
                st.info(
                    explanation["admet"]["interpretation"]
                )
                
                st.write(
                    f"**ADMET Score:** "
                    f"{explanation['admet']['score']:.1f}/100"
                )
                
                st.write(
                    f"**Drug-likeness:** "
                    f"{explanation['admet']['drug_likeness']}"
                )
                
                
                st.markdown(
                    "### 🎯 Ranking Interpretation"
                )
                
                st.info(
                    explanation["ranking"]["interpretation"]
                )
                
                st.write(
                    f"**Overall Score:** "
                    f"{explanation['ranking']['overall_score']:.1f}/100"
                )
                
                st.write(
                    f"**Priority:** "
                    f"{explanation['ranking']['priority']}"
                )
                
                
                st.markdown(
                    "### 🏆 Final Recommendation"
                )
                
                st.success(
                    explanation["recommendation"]
                )
                
                
                st.markdown(
                    "### 📋 Scientific Summary"
                )
                
                st.write(
                    explanation["summary"]
                )

                # ====================================================
                # Complete Analysis
                # ====================================================

                with st.expander(
                    "🔍 View Complete Analysis"
                ):

                    st.json(result)


            except Exception as error:

                st.error(
                    "❌ Molecular analysis failed"
                )

                st.exception(error)


# ============================================================
# TAB 2 — BATCH SCREENING
# ============================================================

with tab2:

    st.header(
        "📂 Batch Molecular Screening"
    )

    st.markdown(
        """
        Upload a CSV file containing a **smiles** column.

        MOLE-AI v2 will process each molecule through:

        **Chemistry → QSAR → ADMET → Candidate Ranking**
        """
    )


    uploaded_file = st.file_uploader(
        "Upload molecular library",
        type=["csv"],
    )


    if uploaded_file is not None:

        try:

            dataframe = pd.read_csv(
                uploaded_file
            )


            st.subheader(
                "📄 Input Dataset"
            )

            st.write(
                f"Number of molecules: {len(dataframe)}"
            )


            st.dataframe(
                dataframe.head(10),
                width="stretch",
                hide_index=True,
            )


            if "smiles" not in dataframe.columns:

                st.error(
                    "❌ CSV must contain a column named 'smiles'."
                )


            else:

                st.success(
                    "✅ SMILES column detected"
                )


                if st.button(
                    "🚀 Run Batch Screening",
                    type="primary",
                ):

                    try:

                        with st.spinner(
                            "Screening molecular library..."
                        ):

                            workflow = (
                                BatchScreeningWorkflow()
                            )

                            results = workflow.screen(
                                dataframe,
                                smiles_column="smiles",
                            )


                        st.success(
                            "✅ Batch screening completed"
                        )


                        st.subheader(
                            "🎯 Ranked Candidates"
                        )


                        st.dataframe(
                            results,
                            width="stretch",
                            hide_index=True,
                        )

                        # --------------------------------------------
                        # Batch Screening Analytics
                        # --------------------------------------------

                        st.markdown(
                            "### 📊 Screening Overview"
                        )

                        # Basic statistics
                        total = len(results)

                        successful = len(
                            results[
                                results["Status"]
                                == "Success"
                            ]
                        )

                        failed = total - successful


                        # Top score
                        if successful > 0:

                            top_score = float(
                                results[
                                    "Overall Score"
                                ].max()
                            )

                        else:

                            top_score = 0.0


                        # Average score
                        if successful > 0:

                            average_score = float(
                                results[
                                    "Overall Score"
                                ].mean()
                            )

                        else:

                            average_score = 0.0


                        # --------------------------------------------
                        # Overview Cards
                        # --------------------------------------------

                        overview_col1, overview_col2, overview_col3, overview_col4 = (
                            st.columns(4)
                        )

                        with overview_col1:

                            st.metric(
                                "Total Molecules",
                                total,
                            )

                        with overview_col2:

                            st.metric(
                                "Successful",
                                successful,
                            )

                        with overview_col3:

                            st.metric(
                                "Top Overall Score",
                                f"{top_score:.1f}",
                            )

                        with overview_col4:

                            st.metric(
                                "Average Score",
                                f"{average_score:.1f}",
                            )


                        st.divider()


                        # --------------------------------------------
                        # Activity Distribution
                        # --------------------------------------------

                        st.markdown(
                            "### 🤖 Activity Distribution"
                        )

                        if (
                            successful > 0
                            and "Activity" in results.columns
                        ):

                            activity_counts = (
                                results[
                                    results["Status"]
                                    == "Success"
                                ]["Activity"]
                                .value_counts()
                            )

                            activity_df = (
                                activity_counts
                                .rename("Molecules")
                                .to_frame()
                            )

                            st.bar_chart(
                                activity_df,
                                y="Molecules",
                                width="stretch",
                            )

                        else:

                            st.info(
                                "No successful activity predictions available."
                            )


                        st.divider()


                        # --------------------------------------------
                        # Priority Distribution
                        # --------------------------------------------

                        st.markdown(
                            "### 🎯 Candidate Priority Distribution"
                        )

                        if (
                            successful > 0
                            and "Priority" in results.columns
                        ):

                            priority_counts = (
                                results[
                                    results["Status"]
                                    == "Success"
                                ]["Priority"]
                                .value_counts()
                            )

                            priority_df = (
                                priority_counts
                                .rename("Molecules")
                                .to_frame()
                            )

                            st.bar_chart(
                                priority_df,
                                y="Molecules",
                                width="stretch",
                            )

                        else:

                            st.info(
                                "No priority results available."
                            )


                        st.divider()


                        # --------------------------------------------
                        # Overall Score Distribution
                        # --------------------------------------------

                        st.markdown(
                            "### 📈 Overall Score Distribution"
                        )

                        if (
                            successful > 0
                            and "Overall Score"
                            in results.columns
                        ):

                            score_chart = (
                                results[
                                    results["Status"]
                                    == "Success"
                                ][
                                    [
                                        "SMILES",
                                        "Overall Score",
                                    ]
                                ]
                                .set_index("SMILES")
                            )

                            st.bar_chart(
                                score_chart,
                                y="Overall Score",
                                width="stretch",
                            )

                        else:

                            st.info(
                                "No successful scores available."
                            )


                        st.divider()


                        # --------------------------------------------
                        # Top Candidates
                        # --------------------------------------------

                        st.markdown(
                            "### 🏆 Top Candidates"
                        )

                        if successful > 0:

                            top_candidates = (
                                results[
                                    results["Status"]
                                    == "Success"
                                ]
                                .sort_values(
                                    "Overall Score",
                                    ascending=False,
                                )
                                .head(10)
                            )


                            # Create a clean display copy
                            top_candidates_display = (
                                top_candidates.copy()
                            )


                            st.dataframe(
                                top_candidates_display,
                                width="stretch",
                                hide_index=True,
                            )

                        else:

                            st.info(
                                "No successful candidates available."
                            )


                        st.divider()


                        # --------------------------------------------
                        # Screening Statistics
                        # --------------------------------------------

                        st.markdown(
                            "### 📋 Screening Statistics"
                        )

                        stats_col1, stats_col2 = (
                            st.columns(2)
                        )

                        with stats_col1:

                            st.metric(
                                "Successful Analyses",
                                successful,
                            )

                        with stats_col2:

                            st.metric(
                                "Failed Analyses",
                                failed,
                            )

                        # --------------------------------------------
                        # Download
                        # --------------------------------------------

                        csv_results = (
                            results.to_csv(
                                index=False
                            )
                        )


                        st.download_button(
                            label=(
                                "⬇️ Download Screening Results"
                            ),
                            data=csv_results,
                            file_name=(
                                "MOLE_AI_v2_screening_results.csv"
                            ),
                            mime="text/csv",
                        )


                    except Exception as error:

                        st.error(
                            "❌ Batch screening failed"
                        )

                        st.exception(error)


        except Exception as error:

            st.error(
                "❌ Could not read CSV file"
            )

            st.exception(error)


# ============================================================
# Footer
# ============================================================

st.divider()

st.caption(
    "MOLE-AI v2 — Computational drug discovery and molecular prioritization"
)
