"""
MOLE-AI v2
AI-Powered Computational Drug Discovery Platform
"""

import streamlit as st
import pandas as pd
from mole_ai.utils.validation import validate_molecular_library

from mole_ai.workflows.drug_discovery import DrugDiscoveryWorkflow
from mole_ai.workflows.batch_screening import BatchScreeningWorkflow
from mole_ai.ranking.comparison import CandidateComparison
from mole_ai.ranking.explanation import CandidateExplainer
from mole_ai.agents.similarity_agent import SimilarityAgent
from mole_ai.utils.export import dataframe_to_csv
from mole_ai.reports.pdf_report import (
    generate_single_molecule_report,
    generate_batch_screening_report,
)

def add_csv_download(dataframe):
    """Display a download button for a DataFrame."""
    csv_data = dataframe_to_csv(dataframe)
    st.download_button(
        label="📥 Download Ranked Results (CSV)",
        data=csv_data,
        file_name="MOLE_AI_ranked_results.csv",
        mime="text/csv",
    )

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

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🏠 Getting Started",
        "🔬 Single Molecule Analysis",
        "📂 Batch Screening",
        "🧬 Molecular Similarity",
    ]
)


# ============================================================
# TAB 0 — GETTING STARTED
# ============================================================

with tab1:

    st.header("🏠 Welcome to MOLE-AI v2")

    st.markdown(
        """
        MOLE-AI is an AI-powered computational drug discovery
        platform for **molecular screening and candidate prioritization**.

        You can use MOLE-AI in two ways:

        **🔬 Single Molecule Analysis**
        - Enter one molecule using a SMILES string.
        - Analyze molecular properties.
        - Predict molecular activity.
        - Evaluate ADMET-related properties.
        - Calculate a candidate prioritization score.

        **📂 Batch Screening**
        - Upload your own CSV file containing molecular SMILES.
        - Screen multiple molecules automatically.
        - Compare molecular activity and ADMET scores.
        - Rank candidates.
        - Identify high-priority molecules.
        - Download the screening results.
        """
    )

    st.divider()

    st.subheader("🚀 How to use MOLE-AI")

    st.markdown(
        """
        **Step 1 — Prepare your molecular data**

        Create a CSV file containing a column named:

        `smiles`

        Example:

        | smiles |
        |---|
        | CCO |
        | CCN |
        | c1ccccc1 |
        | CC(=O)Oc1ccccc1C(=O)O |

        **Step 2 — Upload your CSV**

        Go to the **📂 Batch Screening** tab and upload your file.

        **Step 3 — Run screening**

        MOLE-AI will analyze each valid molecule and generate
        activity, ADMET, molecular-property and prioritization results.

        **Step 4 — Compare candidates**

        Use the ranking and analytics to identify molecules
        that may deserve further computational investigation.

        **Step 5 — Download results**

        Download the complete screening results as a CSV file.
        """
    )

    st.info(
        "💡 MOLE-AI provides computational predictions and "
        "prioritization. Results should be experimentally validated "
        "before making biological or clinical decisions."
    )

# ============================================================
# TAB 2 — SINGLE MOLECULE ANALYSIS
# ============================================================

with tab2:

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

                st.divider()

                # ====================================================
                # Professional PDF Report
                # ====================================================

                st.subheader(
                    "📄 Research Report"
                )

                single_pdf = (
                    generate_single_molecule_report(
                        result,
                        explanation,
                    )
                )
                st.download_button(
                    label="📥 Download Professional PDF Report",
                    data=single_pdf,
                    file_name="MOLE_AI_single_molecule_report.pdf",
                    mime="application/pdf",
                    key="single_molecule_pdf_download",
                )

                # ====================================================
                # ====================================================
                # Molecular Optimization
                # ====================================================

                st.subheader(
                    "🧬 Molecular Optimization"
                )

                optimization = result.get(
                    "optimization",
                    {}
                )

                if optimization:

                    optimization_priority = optimization.get(
                        "optimization_priority",
                        "Not available",
                    )

                    st.markdown(
                        "### 🎯 Optimization Priority"
                    )

                    if optimization_priority == "High":
                        st.error(
                            f"🔴 **{optimization_priority} Priority**"
                        )

                    elif optimization_priority == "Medium":
                        st.warning(
                            f"🟡 **{optimization_priority} Priority**"
                        )

                    else:
                        st.success(
                            f"🟢 **{optimization_priority} Priority**"
                        )

                    st.markdown(
                        "### 💡 Optimization Suggestions"
                    )

                    suggestions = optimization.get(
                        "suggestions",
                        []
                    )

                    for suggestion in suggestions:
                        st.info(
                            f"• {suggestion}"
                        )

                    st.markdown(
                        "### 📊 Optimization Assessment"
                    )

                    opt_col1, opt_col2, opt_col3 = st.columns(3)

                    with opt_col1:
                        st.metric(
                            "Predicted pIC50",
                            f"{optimization.get('predicted_pIC50', 0):.3f}",
                        )

                    with opt_col2:
                        st.metric(
                            "ADMET Score",
                            f"{optimization.get('admet_score', 0):.1f}",
                        )

                    with opt_col3:
                        st.metric(
                            "Overall Score",
                            f"{optimization.get('overall_score', 0):.1f}",
                        )

                    properties = optimization.get(
                        "properties",
                        {}
                    )

                    if properties:

                        st.markdown(
                            "### 🧪 Properties Considered"
                        )

                        properties_df = pd.DataFrame(
                            {
                                "Property": list(properties.keys()),
                                "Value": list(properties.values()),
                            }
                        )

                        st.dataframe(
                            properties_df,
                            width="stretch",
                            hide_index=True,
                        )

                else:

                    st.info(
                        "Molecular optimization analysis is not available."
                    )

                st.divider()

                # ====================================================
                # Molecular Generation
                # ====================================================

                st.subheader(
                    "🧪 Molecular Generation"
                )

                st.caption(
                    "Generate controlled molecular variants from "
                    "the analyzed parent molecule."
                )

                generation = result.get(
                    "generation",
                    []
                )

                if generation:

                    st.markdown(
                        "### 🧬 Generated Candidates"
                    )

                    generation_df = pd.DataFrame(
                        generation
                    )

                    display_columns = [
                        "candidate_id",
                        "smiles",
                        "strategy",
                        "similarity",
                    ]

                    available_columns = [
                        column
                        for column in display_columns
                        if column in generation_df.columns
                    ]

                    st.dataframe(
                        generation_df[available_columns],
                        width="stretch",
                        hide_index=True,
                    )

                    if "similarity" in generation_df.columns:

                        similarity_df = generation_df[
                            [
                                "candidate_id",
                                "similarity",
                            ]
                        ].copy()

                        similarity_df[
                            "similarity_percent"
                        ] = (
                            similarity_df["similarity"] * 100
                        ).round(2)

                        st.markdown(
                            "### 📊 Parent–Candidate Similarity"
                        )

                        st.bar_chart(
                            similarity_df.set_index(
                                "candidate_id"
                            )["similarity_percent"],
                            y="similarity_percent",
                            width="stretch",
                        )

                    generation_csv = (
                        generation_df.to_csv(
                            index=False
                        )
                    )

                    st.download_button(
                        label=(
                            "📥 Download Generated Candidates (CSV)"
                        ),
                        data=generation_csv,
                        file_name=(
                            "MOLE_AI_generated_candidates.csv"
                        ),
                        mime="text/csv",
                    )

                    st.info(
                        "⚠️ Generated molecules are computational "
                        "hypotheses produced by rule-based structural "
                        "transformations. They are not experimentally "
                        "validated compounds and require further "
                        "scientific evaluation."
                    )

                else:

                    st.info(
                        "No generated candidates are available "
                        "for this molecule."
                    )

                st.divider()

                # ====================================================
                # Generated Candidate Evaluation
                # ====================================================

                st.subheader(
                    "🔬 Generated Candidate Evaluation"
                )

                st.caption(
                    "Generated molecules are evaluated using the "
                    "existing QSAR, ADMET, and candidate-ranking "
                    "components."
                )

                evaluated_candidates = result.get(
                    "generated_candidate_evaluation",
                    []
                )

                if evaluated_candidates:

                    evaluation_df = pd.DataFrame(
                        evaluated_candidates
                    )

                    evaluation_columns = [
                        "candidate_id",
                        "smiles",
                        "strategy",
                        "similarity",
                        "predicted_pIC50",
                        "activity_class",
                        "admet_score",
                        "overall_score",
                        "priority",
                    ]

                    available_evaluation_columns = [
                        column
                        for column in evaluation_columns
                        if column in evaluation_df.columns
                    ]

                    display_evaluation_df = evaluation_df[
                        available_evaluation_columns
                    ].copy()

                    if "similarity" in display_evaluation_df.columns:
                        display_evaluation_df[
                            "similarity"
                        ] = (
                            display_evaluation_df[
                                "similarity"
                            ].round(3)
                        )

                    if "predicted_pIC50" in display_evaluation_df.columns:
                        display_evaluation_df[
                            "predicted_pIC50"
                        ] = (
                            display_evaluation_df[
                                "predicted_pIC50"
                            ].round(3)
                        )

                    if "admet_score" in display_evaluation_df.columns:
                        display_evaluation_df[
                            "admet_score"
                        ] = (
                            display_evaluation_df[
                                "admet_score"
                            ].round(1)
                        )

                    if "overall_score" in display_evaluation_df.columns:
                        display_evaluation_df[
                            "overall_score"
                        ] = (
                            display_evaluation_df[
                                "overall_score"
                            ].round(1)
                        )

                    st.dataframe(
                        display_evaluation_df,
                        width="stretch",
                        hide_index=True,
                    )

                    # ------------------------------------------------
                    # Evaluation Summary
                    # ------------------------------------------------

                    st.markdown(
                        "### 📊 Evaluation Summary"
                    )

                    eval_col1, eval_col2, eval_col3 = st.columns(3)

                    with eval_col1:
                        st.metric(
                            "Evaluated Candidates",
                            len(evaluated_candidates),
                        )

                    with eval_col2:
                        best_score = float(
                            evaluation_df[
                                "overall_score"
                            ].max()
                        )

                        st.metric(
                            "Best Overall Score",
                            f"{best_score:.1f}",
                        )

                    with eval_col3:
                        best_candidate = evaluation_df.iloc[
                            evaluation_df[
                                "overall_score"
                            ].idxmax()
                        ]

                        st.metric(
                            "Top Candidate",
                            best_candidate["candidate_id"],
                        )

                    # ------------------------------------------------
                    # Candidate Score Comparison
                    # ------------------------------------------------

                    if "overall_score" in evaluation_df.columns:

                        score_chart_df = evaluation_df[
                            [
                                "candidate_id",
                                "overall_score",
                            ]
                        ].copy()

                        score_chart_df = score_chart_df.set_index(
                            "candidate_id"
                        )

                        st.markdown(
                            "### 🏆 Candidate Overall Scores"
                        )

                        st.bar_chart(
                            score_chart_df,
                            y="overall_score",
                            width="stretch",
                        )

                    # ------------------------------------------------
                    # Download Evaluation Results
                    # ------------------------------------------------

                    evaluation_csv = evaluation_df.to_csv(
                        index=False
                    )

                    st.download_button(
                        label=(
                            "📥 Download Evaluated Candidates (CSV)"
                        ),
                        data=evaluation_csv,
                        file_name=(
                            "MOLE_AI_evaluated_generated_candidates.csv"
                        ),
                        mime="text/csv",
                    )

                    st.info(
                        "⚠️ Evaluation results are computational "
                        "predictions used for candidate prioritization. "
                        "They are not experimental validation of "
                        "biological activity, safety, or efficacy."
                    )

                else:

                    st.info(
                        "No generated candidates were successfully "
                        "evaluated."
                    )

                st.divider()

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
# TAB 3 — BATCH SCREENING
# ============================================================

with tab3:

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

    # ============================================================
    # CSV Template and Upload Instructions
    # ============================================================
    
    st.markdown(
        """
        ### 📋 Prepare Your Molecular Library
    
        Upload a CSV file containing a column named **`smiles`**.
    
        Each row should contain one molecular SMILES string.
    
        **Example:**
    
        | smiles |
        |---|
        | CCO |
        | CCN |
        | c1ccccc1 |
        | CC(=O)Oc1ccccc1C(=O)O |
    
        MOLE-AI will analyze each molecule using:
    
        **SMILES Validation → Molecular Properties → QSAR → ADMET → Ranking**
        """
    )
    
    # ------------------------------------------------------------
    # Download CSV Template
    # ------------------------------------------------------------
    
    template_df = pd.DataFrame(
        {
              "compound_id": ["Compound_001", "Compound_002", "Compound_003", "Compound_004"],
            "smiles": [
                "CCO",
                "CCN",
                "c1ccccc1",
                "CC(=O)Oc1ccccc1C(=O)O",
            ]
        }
    )
    
    template_csv = template_df.to_csv(
        index=False
    )
    
    st.download_button(
        label="📥 Download CSV Template",
        data=template_csv,
        file_name="MOLE_AI_molecular_library_template.csv",
        mime="text/csv",
    )
    
    st.caption(
        "You can download the template, replace the example SMILES "
        "with your own molecules, and upload the file below."
    )
    
    st.divider()
    
    # ------------------------------------------------------------
    # Upload
    # ------------------------------------------------------------
    
    uploaded_file = st.file_uploader(
        "📂 Upload your molecular library",
        type=["csv"],
        help="CSV must contain a column named 'smiles'.",
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
                        # Download ranked screening results
                        results_csv = results.to_csv(index=False)

                        st.download_button(
                            label="📥 Download Ranked Results (CSV)",
                            data=results_csv,
                            file_name="MOLE_AI_ranked_screening_results.csv",
                            mime="text/csv",
                        )

                        # Professional Batch Screening PDF Report
                        batch_pdf = generate_batch_screening_report(
                            results
                        )

                        st.download_button(
                            label="📄 Download Professional PDF Report",
                            data=batch_pdf,
                            file_name="MOLE_AI_batch_screening_report.pdf",
                            mime="application/pdf",
                            key="batch_screening_pdf_download",
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
# TAB 4 — MOLECULAR SIMILARITY
# ============================================================

with tab4:

    st.header("🧬 Molecular Similarity Search")

    st.markdown(
        """
        Compare a query molecule against a molecular library
        using **Morgan fingerprints** and **Tanimoto similarity**.

        Higher similarity values indicate greater structural similarity.
        """
    )

    st.divider()

    similarity_col1, similarity_col2 = st.columns(2)

    with similarity_col1:

        query_smiles = st.text_input(
            "🔬 Query Molecule SMILES",
            placeholder="Example: CCO",
            help="Enter a valid molecular SMILES string.",
        )

    with similarity_col2:

        top_k = st.number_input(
            "🏆 Number of Similar Molecules",
            min_value=1,
            max_value=100,
            value=10,
            step=1,
        )

    st.markdown("### 📂 Molecular Library")

    similarity_file = st.file_uploader(
        "Upload a CSV containing a 'smiles' column",
        type=["csv"],
        key="similarity_library_upload",
        help="Optional compound_id column is supported.",
    )

    if similarity_file is not None:

        try:

            similarity_df = pd.read_csv(
                similarity_file
            )

            st.write(
                f"Library molecules: {len(similarity_df)}"
            )

            st.dataframe(
                similarity_df.head(10),
                width="stretch",
                hide_index=True,
            )

            if "smiles" not in similarity_df.columns:

                st.error(
                    "❌ CSV must contain a column named 'smiles'."
                )

            elif not query_smiles.strip():

                st.warning(
                    "⚠️ Please enter a query molecule SMILES."
                )

            else:

                if st.button(
                    "🔎 Find Similar Molecules",
                    type="primary",
                ):

                    try:

                        with st.spinner(
                            "Calculating molecular similarities..."
                        ):

                            similarity_agent = SimilarityAgent()

                            library_records = (
                                similarity_df.to_dict(
                                    orient="records"
                                )
                            )

                            similarity_results = (
                                similarity_agent.rank_similar(
                                    query_smiles.strip(),
                                    library_records,
                                    top_k=int(top_k),
                                )
                            )

                        if not similarity_results:

                            st.warning(
                                "No valid molecules were found "
                                "in the uploaded library."
                            )

                        else:

                            st.success(
                                "✅ Molecular similarity analysis completed"
                            )

                            similarity_results_df = pd.DataFrame(
                                similarity_results
                            )

                            similarity_results_df[
                                "similarity_percent"
                            ] = (
                                similarity_results_df[
                                    "similarity"
                                ]
                                * 100
                            ).round(2)

                            similarity_results_df = (
                                similarity_results_df[
                                    [
                                        "compound_id",
                                        "smiles",
                                        "similarity",
                                        "similarity_percent",
                                    ]
                                ]
                            )

                            st.subheader(
                                "🏆 Most Similar Molecules"
                            )

                            st.dataframe(
                                similarity_results_df,
                                width="stretch",
                                hide_index=True,
                            )

                            st.markdown(
                                "### 📊 Similarity Scores"
                            )

                            chart_df = (
                                similarity_results_df[
                                    [
                                        "compound_id",
                                        "similarity_percent",
                                    ]
                                ]
                                .set_index("compound_id")
                            )

                            st.bar_chart(
                                chart_df,
                                y="similarity_percent",
                                width="stretch",
                            )

                            similarity_csv = (
                                similarity_results_df.to_csv(
                                    index=False
                                )
                            )

                            st.download_button(
                                label=(
                                    "📥 Download Similarity Results (CSV)"
                                ),
                                data=similarity_csv,
                                file_name=(
                                    "MOLE_AI_similarity_results.csv"
                                ),
                                mime="text/csv",
                            )

                    except Exception as error:

                        st.error(
                            "❌ Molecular similarity analysis failed"
                        )

                        st.exception(error)

        except Exception as error:

            st.error(
                "❌ Could not read molecular library"
            )

            st.exception(error)


# ============================================================
# Footer
# ============================================================

st.divider()

st.caption(
    "MOLE-AI v2 — Computational drug discovery and molecular prioritization"
)
