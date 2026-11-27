"""
MOLE-AI v2
Computational drug discovery platform.
"""

import hmac
import json

import pandas as pd
import streamlit as st

from mole_ai.agents.similarity_agent import SimilarityAgent
from mole_ai.ranking.explanation import CandidateExplainer
from mole_ai.reports.pdf_report import (
    generate_batch_screening_report,
    generate_single_molecule_report,
)
from mole_ai.ui import components as ui
from mole_ai.workflows.batch_screening import BatchScreeningWorkflow
from mole_ai.workflows.drug_discovery import DrugDiscoveryWorkflow

FREE_BATCH_LIMIT = 5
PAID_BATCH_LIMIT = 500

EXAMPLES = {
    "Aspirin": "CC(=O)Oc1ccccc1C(=O)O",
    "Caffeine": "Cn1cnc2c1c(=O)n(C)c(=O)n2C",
    "Ibuprofen": "CC(C)Cc1ccc(cc1)C(C)C(=O)O",
}

SCORE = st.column_config.ProgressColumn
NUM = st.column_config.NumberColumn


st.set_page_config(page_title="MOLE-AI", page_icon="⬡", layout="wide")
ui.apply_theme()


# ============================================================
# Helpers
# ============================================================


def read_library(uploaded) -> pd.DataFrame:
    """Read a CSV and normalise column names (SMILES, Smiles, ' smiles ')."""
    frame = pd.read_csv(uploaded)
    frame.columns = [str(c).strip().lower() for c in frame.columns]
    return frame


def check_paid_access() -> bool:
    """Check the commercial batch-analysis access code."""
    access_code = st.secrets.get("MOLE_AI_ACCESS_CODE", "")

    if not access_code:
        st.warning("Paid access is not configured yet. Contact MOLE-AI for access.")
        return False

    entered = st.text_input(
        "Access code",
        type="password",
        help="The code you received after purchase.",
    )
    if not entered:
        return False
    if hmac.compare_digest(entered.strip(), str(access_code).strip()):
        st.success("Access confirmed.")
        return True
    st.error("That access code is not valid.")
    return False


def round_columns(frame: pd.DataFrame, spec: dict) -> pd.DataFrame:
    for column, digits in spec.items():
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce").round(digits)
    return frame


def kv_table(mapping: dict) -> None:
    frame = pd.DataFrame(list(mapping.items()), columns=["Property", "Value"])
    frame["Value"] = frame["Value"].astype(str)
    st.dataframe(frame, width="stretch", hide_index=True)


# ============================================================
# Masthead and navigation
# ============================================================

ui.masthead()

tab_home, tab_single, tab_batch, tab_sim = st.tabs(
    ["Overview", "Single molecule", "Batch screening", "Similarity"]
)


# ============================================================
# Overview
# ============================================================

with tab_home:
    ui.hero(
        "Screen, rank and refine <em>drug candidates</em>.",
        "Molecular descriptors, QSAR activity and ADMET profiling "
        "brought together in one prioritisation workflow.",
    )

    ui.feature_cards(
        [
            (
                "01",
                "Single molecule",
                "Profile one compound: activity, ADMET, ranking and "
                "suggested analogues.",
                "Input — one SMILES string",
            ),
            (
                "02",
                "Batch screening",
                "Rank a whole library and export the shortlist as CSV "
                "or a PDF report.",
                f"Input — CSV, free up to {FREE_BATCH_LIMIT} molecules",
            ),
            (
                "03",
                "Similarity",
                "Find the library compounds closest in structure to a "
                "query molecule.",
                "Input — SMILES and a CSV library",
            ),
        ]
    )

    ui.subheading("How it works")
    ui.steps(
        [
            ("Prepare", "A CSV with a smiles column. compound_id is optional."),
            ("Upload", "Drop the file into Batch screening."),
            ("Screen", "Each molecule is validated, described, predicted and scored."),
            ("Export", "Download the ranked results or a PDF report."),
        ]
    )


# ============================================================
# Single molecule
# ============================================================


def _use_example(smiles: str) -> None:
    st.session_state.smiles_input = smiles
    st.session_state.run_single = True


def run_single(smiles: str) -> None:
    result = DrugDiscoveryWorkflow().analyze(smiles)
    explanation = CandidateExplainer().explain(result)
    st.session_state.single = {
        "smiles": smiles,
        "result": result,
        "explanation": explanation,
        "pdf": generate_single_molecule_report(result, explanation),
    }


def render_single(data: dict) -> None:
    result = data["result"]
    explanation = data["explanation"]
    ranking = result["ranking"]
    qsar = result["qsar"]
    admet = result["admet"]
    descriptors = result["chemistry"]["descriptors"]

    ui.molecule_line(data["smiles"], ranking["priority"])

    ui.stats(
        [
            ("Overall score", f"{ranking['overall_score']:.1f}", "/ 100"),
            ("Predicted pIC50", f"{qsar['predicted_pIC50']:.2f}", None),
            ("ADMET score", f"{admet['admet_score']:.1f}", "/ 100"),
            ("Activity", str(qsar["activity_class"]).replace(" Activity", ""), None),
        ]
    )

    if explanation.get("recommendation"):
        ui.note(explanation["recommendation"], title="Recommendation")

    t_sum, t_props, t_opt, t_ana, t_exp = st.tabs(
        ["Summary", "Properties", "Optimisation", "Analogues", "Export"]
    )

    # ---- Summary ------------------------------------------------------
    with t_sum:
        left, right = st.columns([2, 3], gap="large")
        with left:
            ui.subheading("Score profile")
            bars = [
                ("Activity", ranking["activity_score"]),
                ("ADMET", ranking["admet_score"]),
            ]
            props_score = explanation.get("molecular_properties", {}).get("score")
            if props_score is not None:
                bars.append(("Molecular properties", props_score))
            bars.append(("Overall", ranking["overall_score"]))
            ui.score_bars(bars)
        with right:
            ui.subheading("Interpretation")
            ui.definition_list(
                [
                    ("Activity", explanation["activity"].get("interpretation")),
                    ("ADMET", explanation["admet"].get("interpretation")),
                    ("Ranking", explanation["ranking"].get("interpretation")),
                ]
            )
            if explanation.get("summary"):
                with st.expander("Full scientific summary"):
                    st.write(explanation["summary"])

    # ---- Properties ---------------------------------------------------
    with t_props:
        left, right = st.columns(2, gap="large")
        with left:
            ui.subheading("Molecular descriptors")
            kv_table(descriptors)
        with right:
            ui.subheading("ADMET")
            st.html(
                f'<div class="mol">Drug-likeness '
                f'{ui.badge_html(admet["drug_likeness"])}</div>'
            )
            if "properties" in admet:
                kv_table(admet["properties"])
            ui.small(f"QSAR model: {qsar['model']}")

    # ---- Optimisation -------------------------------------------------
    with t_opt:
        optimization = result.get("optimization") or {}
        if not optimization:
            ui.small("No optimisation analysis is available for this molecule.")
        else:
            level = optimization.get("optimization_priority", "Not available")
            tone = {"High": "bad", "Medium": "warn"}.get(level, "good")
            st.html(
                f'<div class="mol">Optimisation need '
                f'{ui.badge_html(level, tone)}</div>'
            )
            left, right = st.columns([3, 2], gap="large")
            with left:
                ui.subheading("Suggestions")
                suggestions = optimization.get("suggestions", [])
                if suggestions:
                    st.markdown("\n".join(f"{i}. {s}" for i, s in enumerate(suggestions, 1)))
                else:
                    ui.small("No changes suggested.")
            with right:
                properties = optimization.get("properties", {})
                if properties:
                    ui.subheading("Properties considered")
                    kv_table(properties)

    # ---- Analogues ----------------------------------------------------
    with t_ana:
        evaluated = result.get("generated_candidate_evaluation") or []
        generated = result.get("generation") or []

        if evaluated:
            frame = pd.DataFrame(evaluated)
            best = frame.loc[frame["overall_score"].idxmax()]
            ui.stats(
                [
                    ("Analogues", len(frame), None),
                    ("Best overall score", f"{best['overall_score']:.1f}", "/ 100"),
                    ("Top analogue", best["candidate_id"], None),
                ]
            )
            columns = [
                c
                for c in [
                    "candidate_id", "smiles", "strategy", "similarity",
                    "predicted_pIC50", "admet_score", "overall_score", "priority",
                ]
                if c in frame.columns
            ]
            view = round_columns(
                frame[columns].copy(),
                {"similarity": 3, "predicted_pIC50": 2, "admet_score": 1, "overall_score": 1},
            ).sort_values("overall_score", ascending=False)
            st.dataframe(
                view,
                width="stretch",
                hide_index=True,
                column_config={
                    "candidate_id": "ID",
                    "smiles": "SMILES",
                    "strategy": "Strategy",
                    "similarity": SCORE("Similarity", min_value=0, max_value=1, format="%.2f"),
                    "predicted_pIC50": NUM("pIC50", format="%.2f"),
                    "admet_score": NUM("ADMET", format="%.1f"),
                    "overall_score": SCORE("Overall", min_value=0, max_value=100, format="%.1f"),
                    "priority": "Priority",
                },
            )
            st.download_button(
                "Download analogues (CSV)",
                frame.to_csv(index=False),
                file_name="MOLE_AI_evaluated_generated_candidates.csv",
                mime="text/csv",
                on_click="ignore",
            )
        elif generated:
            st.dataframe(pd.DataFrame(generated), width="stretch", hide_index=True)
        else:
            ui.small("No analogues could be generated for this molecule.")

        if evaluated or generated:
            ui.small(
                "Analogues are rule-based structural variants with predicted "
                "scores. They are hypotheses, not validated compounds."
            )

    # ---- Export -------------------------------------------------------
    with t_exp:
        ui.subheading("Downloads")
        c1, c2, _ = st.columns([1, 1, 2])
        with c1:
            st.download_button(
                "PDF report",
                data["pdf"],
                file_name="MOLE_AI_single_molecule_report.pdf",
                mime="application/pdf",
                type="primary",
                on_click="ignore",
                width="stretch",
            )
        with c2:
            st.download_button(
                "Raw data (JSON)",
                json.dumps(result, indent=2, default=str),
                file_name="MOLE_AI_analysis.json",
                mime="application/json",
                on_click="ignore",
                width="stretch",
            )
        with st.expander("View raw analysis"):
            st.json(result, expanded=False)


with tab_single:
    ui.section(
        "Single molecule",
        kicker="Analyse",
        note="Enter a SMILES string to profile one compound.",
    )

    with st.container():
        col_in, col_btn = st.columns([5, 1], vertical_alignment="bottom")
        with col_in:
            smiles = st.text_input(
                "SMILES",
                key="smiles_input",
                placeholder="e.g. CC(=O)Oc1ccccc1C(=O)O",
            )
        with col_btn:
            analyze = st.button("Analyse", type="primary", width="stretch")

        ex_cols = st.columns([0.6, 0.7, 0.7, 0.8, 6])
        ex_cols[0].html('<div class="small" style="padding-top:6px">Try</div>')
        for col, (name, value) in zip(ex_cols[1:4], EXAMPLES.items()):
            col.button(name, type="tertiary", on_click=_use_example, args=(value,), key=f"ex_{name}")

    if analyze or st.session_state.pop("run_single", False):
        smiles = st.session_state.get("smiles_input", "").strip()
        if not smiles:
            st.warning("Enter a SMILES string first.")
        else:
            try:
                with st.spinner("Analysing molecule…"):
                    run_single(smiles)
            except ValueError as error:
                st.session_state.pop("single", None)
                st.warning(f"That SMILES string could not be parsed. {error}")
            except Exception as error:  # noqa: BLE001
                st.session_state.pop("single", None)
                st.error("The analysis failed.")
                st.exception(error)

    if "single" in st.session_state:
        st.divider()
        render_single(st.session_state.single)


# ============================================================
# Batch screening
# ============================================================


def render_batch(results: pd.DataFrame, pdf: bytes) -> None:
    ok = results[results["Status"] == "Success"]
    total, successful = len(results), len(ok)
    top = float(ok["Overall Score"].max()) if successful else 0.0
    mean = float(ok["Overall Score"].mean()) if successful else 0.0

    ui.stats(
        [
            ("Screened", total, None),
            ("Successful", successful, f"of {total}"),
            ("Top score", f"{top:.1f}", "/ 100"),
            ("Mean score", f"{mean:.1f}", "/ 100"),
        ]
    )

    c1, c2, _ = st.columns([1, 1, 2])
    with c1:
        st.download_button(
            "Download results (CSV)",
            results.to_csv(index=False),
            file_name="MOLE_AI_ranked_screening_results.csv",
            mime="text/csv",
            type="primary",
            on_click="ignore",
            width="stretch",
        )
    with c2:
        st.download_button(
            "PDF report",
            pdf,
            file_name="MOLE_AI_batch_screening_report.pdf",
            mime="application/pdf",
            on_click="ignore",
            width="stretch",
        )

    labels = ["Ranking", "Distribution"]
    failed = results[results["Status"] != "Success"]
    if len(failed):
        labels.append(f"Errors ({len(failed)})")
    tabs = st.tabs(labels)

    with tabs[0]:
        ranked = ok.sort_values("Overall Score", ascending=False)
        st.dataframe(
            ranked.drop(columns=["Status"]),
            width="stretch",
            hide_index=True,
            column_config={
                "SMILES": st.column_config.TextColumn("SMILES", width="medium"),
                "Predicted pIC50": NUM("pIC50", format="%.2f"),
                "ADMET Score": NUM("ADMET", format="%.1f"),
                "Overall Score": SCORE("Overall", min_value=0, max_value=100, format="%.1f"),
                "Best Generated Score": NUM("Best analogue score", format="%.1f"),
                "Best Generated ADMET": NUM("Best analogue ADMET", format="%.1f"),
                "Best Candidate Similarity": NUM("Analogue similarity", format="%.2f"),
            },
        )

    with tabs[1]:
        if not successful:
            ui.small("No successful predictions to chart.")
        else:
            left, right = st.columns(2, gap="large")
            with left:
                ui.subheading("Activity")
                st.bar_chart(
                    ok["Activity"].value_counts().rename("Molecules"),
                    color=ui.ACCENT,
                    horizontal=True,
                    height=220,
                )
            with right:
                ui.subheading("Priority")
                st.bar_chart(
                    ok["Priority"].value_counts().rename("Molecules"),
                    color=ui.ACCENT,
                    horizontal=True,
                    height=220,
                )
            ui.subheading("Overall score by compound")
            label = "Compound ID" if "Compound ID" in ok.columns else "SMILES"
            st.bar_chart(
                ok.sort_values("Overall Score", ascending=False).set_index(label)["Overall Score"],
                color=ui.ACCENT,
                height=280,
            )

    if len(failed):
        with tabs[2]:
            st.dataframe(
                failed[[c for c in ["Compound ID", "SMILES", "Status"] if c in failed.columns]],
                width="stretch",
                hide_index=True,
            )


with tab_batch:
    ui.section(
        "Batch screening",
        kicker="Screen",
        note="Rank a compound library by predicted activity and ADMET profile.",
    )

    left, right = st.columns([2, 3], gap="large")

    with left:
        ui.subheading("Prepare your file")
        st.markdown(
            "One row per molecule, with a `smiles` column. "
            "A `compound_id` column is optional."
        )
        template = pd.DataFrame(
            {
                "compound_id": ["Compound_001", "Compound_002", "Compound_003", "Compound_004"],
                "smiles": ["CCO", "CCN", "c1ccccc1", "CC(=O)Oc1ccccc1C(=O)O"],
            }
        )
        st.download_button(
            "Download CSV template",
            template.to_csv(index=False),
            file_name="MOLE_AI_molecular_library_template.csv",
            mime="text/csv",
            on_click="ignore",
        )

    with right:
        uploaded = st.file_uploader("Molecular library (CSV)", type=["csv"])

    if uploaded is None:
        with left:
            ui.plans(FREE_BATCH_LIMIT, PAID_BATCH_LIMIT)
        st.session_state.pop("batch", None)
    else:
        try:
            library = read_library(uploaded)
        except Exception as error:  # noqa: BLE001
            st.error("That file could not be read as CSV.")
            st.exception(error)
            library = None

        if library is not None:
            count = len(library)
            tier = "free" if count <= FREE_BATCH_LIMIT else "paid"

            with left:
                ui.plans(FREE_BATCH_LIMIT, PAID_BATCH_LIMIT, active=tier)

            with right:
                with st.expander(f"Preview — {count} molecules"):
                    st.dataframe(library.head(10), width="stretch", hide_index=True)

                run_batch = False
                if "smiles" not in library.columns:
                    st.error("No `smiles` column found in this file.")
                elif count > PAID_BATCH_LIMIT:
                    st.error(
                        f"This file has {count} molecules; the limit is "
                        f"{PAID_BATCH_LIMIT}. Contact MOLE-AI for larger libraries."
                    )
                elif tier == "paid":
                    ui.small(f"{count} molecules — a paid batch (€49) is required.")
                    if check_paid_access():
                        run_batch = st.button("Run screening", type="primary")
                else:
                    run_batch = st.button("Run screening", type="primary")

            file_id = (uploaded.name, uploaded.size)
            if st.session_state.get("batch", {}).get("file") != file_id:
                st.session_state.pop("batch", None)

            if run_batch:
                try:
                    with st.spinner(f"Screening {count} molecules…"):
                        results = BatchScreeningWorkflow().screen(library, smiles_column="smiles")
                        st.session_state.batch = {
                            "file": file_id,
                            "results": results,
                            "pdf": generate_batch_screening_report(results),
                        }
                except Exception as error:  # noqa: BLE001
                    st.error("Batch screening failed.")
                    st.exception(error)

            if "batch" in st.session_state:
                st.divider()
                render_batch(
                    st.session_state.batch["results"],
                    st.session_state.batch["pdf"],
                )


# ============================================================
# Similarity
# ============================================================

with tab_sim:
    ui.section(
        "Similarity search",
        kicker="Compare",
        note="Rank a library by structural similarity to a query molecule "
        "(Morgan fingerprints, Tanimoto coefficient).",
    )

    c1, c2 = st.columns([4, 1], vertical_alignment="bottom")
    with c1:
        query = st.text_input("Query SMILES", placeholder="e.g. CC(=O)Oc1ccccc1C(=O)O")
    with c2:
        top_k = st.number_input("Results", min_value=1, max_value=100, value=10, step=1)

    sim_file = st.file_uploader(
        "Library (CSV with a smiles column)",
        type=["csv"],
        key="similarity_library_upload",
    )

    if sim_file is None:
        st.session_state.pop("similarity", None)
    else:
        try:
            sim_library = read_library(sim_file)
        except Exception as error:  # noqa: BLE001
            st.error("That file could not be read as CSV.")
            st.exception(error)
            sim_library = None

        if sim_library is not None:
            if "smiles" not in sim_library.columns:
                st.error("No `smiles` column found in this file.")
            else:
                ui.small(f"{len(sim_library)} molecules in library.")
                if st.button("Find similar molecules", type="primary", disabled=not query.strip()):
                    try:
                        with st.spinner("Comparing fingerprints…"):
                            matches = SimilarityAgent().rank_similar(
                                query.strip(),
                                sim_library.to_dict(orient="records"),
                                top_k=int(top_k),
                            )
                        st.session_state.similarity = matches
                    except Exception as error:  # noqa: BLE001
                        st.session_state.pop("similarity", None)
                        st.error("Similarity search failed.")
                        st.exception(error)

    matches = st.session_state.get("similarity")
    if matches is not None:
        st.divider()
        if not matches:
            st.warning("No valid molecules were found in the library.")
        else:
            frame = pd.DataFrame(matches)[["compound_id", "smiles", "similarity"]]
            st.dataframe(
                frame,
                width="stretch",
                hide_index=True,
                column_config={
                    "compound_id": "Compound",
                    "smiles": "SMILES",
                    "similarity": SCORE("Tanimoto similarity", min_value=0, max_value=1, format="%.3f"),
                },
            )
            st.download_button(
                "Download results (CSV)",
                frame.to_csv(index=False),
                file_name="MOLE_AI_similarity_results.csv",
                mime="text/csv",
                on_click="ignore",
            )


ui.footer()
