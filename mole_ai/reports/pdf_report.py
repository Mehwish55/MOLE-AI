"""
MOLE-AI v2 Professional PDF Report Generator.

Generates research-oriented PDF reports for computational
molecular analysis and batch screening.
"""

from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


def _format_value(value):
    """Convert report values into readable text."""

    if value is None:
        return "N/A"

    if isinstance(value, float):
        return f"{value:.3f}"

    return str(value)


def _section_title(text, styles):
    """Create a consistent section heading."""

    return Paragraph(
        text,
        styles["SectionTitle"],
    )


def _table(data, styles, column_widths=None):
    """Create a professionally formatted table."""

    table = Table(
        data,
        colWidths=column_widths,
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#E8EEF5"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1F2937"),
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#CBD5E1"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    return table


def generate_single_molecule_report(
    result: dict,
    explanation: dict | None = None,
) -> bytes:
    """
    Generate a professional PDF report for one molecule.

    Parameters
    ----------
    result:
        Output dictionary from DrugDiscoveryWorkflow.analyze().

    explanation:
        Optional output from CandidateExplainer.explain().

    Returns
    -------
    bytes
        PDF document as bytes.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="MOLE-AI v2 Computational Molecular Analysis Report",
        author="MOLE-AI",
    )

    base_styles = getSampleStyleSheet()

    styles = {
        "Title": ParagraphStyle(
            "MOLETitle",
            parent=base_styles["Title"],
            alignment=TA_CENTER,
            fontSize=22,
            leading=27,
            spaceAfter=8,
        ),
        "Subtitle": ParagraphStyle(
            "MOLESubtitle",
            parent=base_styles["Normal"],
            alignment=TA_CENTER,
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#4B5563"),
            spaceAfter=18,
        ),
        "SectionTitle": ParagraphStyle(
            "MOLESectionTitle",
            parent=base_styles["Heading2"],
            fontSize=14,
            leading=18,
            spaceBefore=12,
            spaceAfter=8,
            textColor=colors.HexColor("#1F2937"),
        ),
        "Body": ParagraphStyle(
            "MOLEBody",
            parent=base_styles["BodyText"],
            fontSize=9.5,
            leading=14,
            spaceAfter=7,
        ),
        "Small": ParagraphStyle(
            "MOLESmall",
            parent=base_styles["BodyText"],
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#4B5563"),
        ),
    }

    story = []

    smiles = result.get("smiles", "N/A")
    qsar = result.get("qsar", {})
    admet = result.get("admet", {})
    chemistry = result.get("chemistry", {})
    ranking = result.get("ranking", {})

    descriptors = chemistry.get("descriptors", {})

    generated_date = datetime.now().strftime(
        "%d %B %Y, %H:%M"
    )

    # ---------------------------------------------------------
    # Header
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "MOLE-AI v2",
            styles["Title"],
        )
    )

    story.append(
        Paragraph(
            "Computational Molecular Analysis Report",
            styles["Subtitle"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Report generated:</b> {generated_date}",
            styles["Small"],
        )
    )

    story.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # Molecule information
    # ---------------------------------------------------------

    story.append(
        _section_title(
            "1. Molecule Information",
            styles,
        )
    )

    molecule_data = [
        ["Parameter", "Value"],
        ["SMILES", smiles],
    ]

    formula = descriptors.get(
        "molecular_formula",
        descriptors.get("Molecular Formula", "N/A"),
    )

    molecule_data.append(
        ["Molecular Formula", _format_value(formula)]
    )

    story.append(
        _table(
            molecule_data,
            styles,
            [55 * mm, 115 * mm],
        )
    )

    # ---------------------------------------------------------
    # Executive assessment
    # ---------------------------------------------------------

    story.append(
        _section_title(
            "2. Executive Assessment",
            styles,
        )
    )

    assessment_data = [
        ["Metric", "Result"],
        [
            "Predicted pIC50",
            _format_value(
                qsar.get("predicted_pIC50")
            ),
        ],
        [
            "Activity Classification",
            _format_value(
                qsar.get("activity_class")
            ),
        ],
        [
            "ADMET Score",
            _format_value(
                admet.get("admet_score")
            ),
        ],
        [
            "Overall Score",
            _format_value(
                ranking.get("overall_score")
            ),
        ],
        [
            "Priority",
            _format_value(
                ranking.get("priority")
            ),
        ],
    ]

    story.append(
        _table(
            assessment_data,
            styles,
            [65 * mm, 105 * mm],
        )
    )

    # ---------------------------------------------------------
    # Molecular properties
    # ---------------------------------------------------------

    story.append(
        _section_title(
            "3. Molecular Properties",
            styles,
        )
    )

    property_data = [
        ["Property", "Value"]
    ]

    for name, value in descriptors.items():
        property_data.append(
            [
                str(name),
                _format_value(value),
            ]
        )

    if len(property_data) > 1:
        story.append(
            _table(
                property_data,
                styles,
                [75 * mm, 95 * mm],
            )
        )

    # ---------------------------------------------------------
    # QSAR
    # ---------------------------------------------------------

    story.append(
        _section_title(
            "4. QSAR Activity Prediction",
            styles,
        )
    )

    qsar_data = [
        ["Parameter", "Value"],
        [
            "Predicted pIC50",
            _format_value(
                qsar.get("predicted_pIC50")
            ),
        ],
        [
            "Activity Classification",
            _format_value(
                qsar.get("activity_class")
            ),
        ],
        [
            "Model",
            _format_value(
                qsar.get("model")
            ),
        ],
    ]

    story.append(
        _table(
            qsar_data,
            styles,
            [65 * mm, 105 * mm],
        )
    )

    # ---------------------------------------------------------
    # ADMET
    # ---------------------------------------------------------

    story.append(
        _section_title(
            "5. ADMET / Drug-Likeness Assessment",
            styles,
        )
    )

    admet_data = [
        ["Parameter", "Value"],
        [
            "ADMET Score",
            _format_value(
                admet.get("admet_score")
            ),
        ],
        [
            "Drug-likeness",
            _format_value(
                admet.get("drug_likeness")
            ),
        ],
    ]

    for name, value in admet.get(
        "properties",
        {},
    ).items():
        admet_data.append(
            [
                str(name),
                _format_value(value),
            ]
        )

    story.append(
        _table(
            admet_data,
            styles,
            [65 * mm, 105 * mm],
        )
    )

    # ---------------------------------------------------------
    # Candidate prioritization
    # ---------------------------------------------------------

    story.append(
        _section_title(
            "6. Candidate Prioritization",
            styles,
        )
    )

    ranking_data = [
        ["Metric", "Score / Result"],
        [
            "Activity Score",
            _format_value(
                ranking.get("activity_score")
            ),
        ],
        [
            "ADMET Score",
            _format_value(
                ranking.get("admet_score")
            ),
        ],
        [
            "Molecular Property Score",
            _format_value(
                ranking.get("property_score")
            ),
        ],
        [
            "Overall Score",
            _format_value(
                ranking.get("overall_score")
            ),
        ],
        [
            "Priority",
            _format_value(
                ranking.get("priority")
            ),
        ],
    ]

    story.append(
        _table(
            ranking_data,
            styles,
            [75 * mm, 95 * mm],
        )
    )

    # ---------------------------------------------------------
    # Explainability
    # ---------------------------------------------------------

    if explanation:

        story.append(
            _section_title(
                "7. AI Candidate Explainability",
                styles,
            )
        )

        activity = explanation.get(
            "activity",
            {},
        )

        admet_explanation = explanation.get(
            "admet",
            {},
        )

        ranking_explanation = explanation.get(
            "ranking",
            {},
        )

        recommendation = explanation.get(
            "recommendation",
            "",
        )

        story.append(
            Paragraph(
                "<b>Activity Interpretation</b>",
                styles["Body"],
            )
        )

        story.append(
            Paragraph(
                str(
                    activity.get(
                        "interpretation",
                        "N/A",
                    )
                ),
                styles["Body"],
            )
        )

        story.append(
            Paragraph(
                "<b>ADMET Interpretation</b>",
                styles["Body"],
            )
        )

        story.append(
            Paragraph(
                str(
                    admet_explanation.get(
                        "interpretation",
                        "N/A",
                    )
                ),
                styles["Body"],
            )
        )

        story.append(
            Paragraph(
                "<b>Ranking Interpretation</b>",
                styles["Body"],
            )
        )

        story.append(
            Paragraph(
                str(
                    ranking_explanation.get(
                        "interpretation",
                        "N/A",
                    )
                ),
                styles["Body"],
            )
        )

        story.append(
            Paragraph(
                "<b>Final Recommendation</b>",
                styles["Body"],
            )
        )

        story.append(
            Paragraph(
                str(recommendation),
                styles["Body"],
            )
        )

    # ---------------------------------------------------------
    # Scientific summary
    # ---------------------------------------------------------

    if explanation:

        story.append(
            _section_title(
                "8. Scientific Summary",
                styles,
            )
        )

        story.append(
            Paragraph(
                str(
                    explanation.get(
                        "summary",
                        "N/A",
                    )
                ),
                styles["Body"],
            )
        )

    # ---------------------------------------------------------
    # Methodology
    # ---------------------------------------------------------

    story.append(
        _section_title(
            "9. Computational Methodology",
            styles,
        )
    )

    methodology = (
        "MOLE-AI v2 integrates molecular descriptors, "
        "machine-learning-based QSAR prediction, "
        "computational ADMET assessment, and multi-objective "
        "candidate prioritization. Molecular fingerprints "
        "and cheminformatics descriptors are used to support "
        "computational molecular analysis."
    )

    story.append(
        Paragraph(
            methodology,
            styles["Body"],
        )
    )

    # ---------------------------------------------------------
    # Limitations
    # ---------------------------------------------------------

    story.append(
        _section_title(
            "10. Scientific Limitations and Disclaimer",
            styles,
        )
    )

    disclaimer = (
        "<b>Research-use disclaimer:</b> MOLE-AI v2 provides "
        "computational predictions intended to support research "
        "prioritization. Predictions are not experimental "
        "measurements and should not be interpreted as evidence "
        "of biological activity, therapeutic efficacy, safety, "
        "or clinical suitability. Results should be independently "
        "validated using appropriate experimental methods before "
        "biological, therapeutic, or clinical decisions."
    )

    story.append(
        Paragraph(
            disclaimer,
            styles["Body"],
        )
    )

    # ---------------------------------------------------------
    # Footer
    # ---------------------------------------------------------

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "MOLE-AI v2 — Computational drug discovery and "
            "molecular prioritization",
            styles["Small"],
        )
    )

    document.build(story)

    return buffer.getvalue()


def generate_batch_screening_report(
    results,
) -> bytes:
    """
    Generate a professional PDF report for batch screening.

    Parameters
    ----------
    results:
        Pandas DataFrame containing batch screening results.

    Returns
    -------
    bytes
        PDF document as bytes.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="MOLE-AI v2 Batch Screening Report",
        author="MOLE-AI",
    )

    base_styles = getSampleStyleSheet()

    styles = {
        "Title": ParagraphStyle(
            "BatchTitle",
            parent=base_styles["Title"],
            alignment=TA_CENTER,
            fontSize=21,
            leading=25,
            spaceAfter=8,
        ),
        "Subtitle": ParagraphStyle(
            "BatchSubtitle",
            parent=base_styles["Normal"],
            alignment=TA_CENTER,
            fontSize=10,
            textColor=colors.HexColor("#4B5563"),
            spaceAfter=16,
        ),
        "SectionTitle": ParagraphStyle(
            "BatchSectionTitle",
            parent=base_styles["Heading2"],
            fontSize=13,
            leading=17,
            spaceBefore=10,
            spaceAfter=7,
        ),
        "Body": ParagraphStyle(
            "BatchBody",
            parent=base_styles["BodyText"],
            fontSize=9,
            leading=13,
            spaceAfter=6,
        ),
        "Small": ParagraphStyle(
            "BatchSmall",
            parent=base_styles["BodyText"],
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#4B5563"),
        ),
    }

    story = []

    generated_date = datetime.now().strftime(
        "%d %B %Y, %H:%M"
    )

    story.append(
        Paragraph(
            "MOLE-AI v2",
            styles["Title"],
        )
    )

    story.append(
        Paragraph(
            "Batch Molecular Screening Report",
            styles["Subtitle"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Report generated:</b> {generated_date}",
            styles["Small"],
        )
    )

    story.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    story.append(
        _section_title(
            "1. Screening Summary",
            styles,
        )
    )

    total = len(results)

    successful = (
        int(
            (results["Status"] == "Success").sum()
        )
        if "Status" in results.columns
        else total
    )

    summary_data = [
        ["Metric", "Value"],
        ["Total molecules", str(total)],
        ["Successfully analyzed", str(successful)],
        ["Failed / invalid", str(total - successful)],
    ]

    story.append(
        _table(
            summary_data,
            styles,
            [80 * mm, 90 * mm],
        )
    )

    # ---------------------------------------------------------
    # Top candidates
    # ---------------------------------------------------------

    story.append(
        _section_title(
            "2. Top Ranked Candidates",
            styles,
        )
    )

    columns = [
        "Rank",
        "Compound ID",
        "Predicted pIC50",
        "ADMET Score",
        "Overall Score",
        "Priority",
    ]

    available_columns = [
        column
        for column in columns
        if column in results.columns
    ]

    table_data = [
        available_columns
    ]

    for _, row in results.head(20).iterrows():

        table_data.append(
            [
                _format_value(row.get(column))
                for column in available_columns
            ]
        )

    story.append(
        _table(
            table_data,
            styles,
        )
    )

    # ---------------------------------------------------------
    # Interpretation
    # ---------------------------------------------------------

    story.append(
        _section_title(
            "3. Computational Interpretation",
            styles,
        )
    )

    story.append(
        Paragraph(
            "Candidates are ranked using computational activity, "
            "ADMET, molecular-property, and prioritization metrics. "
            "Higher-ranked candidates may warrant additional "
            "computational or experimental investigation.",
            styles["Body"],
        )
    )

    # ---------------------------------------------------------
    # Disclaimer
    # ---------------------------------------------------------

    story.append(
        _section_title(
            "4. Scientific Limitations and Disclaimer",
            styles,
        )
    )

    story.append(
        Paragraph(
            "<b>Research-use disclaimer:</b> MOLE-AI v2 provides "
            "computational predictions intended to support research "
            "prioritization. Results are not experimental measurements "
            "and require independent experimental validation before "
            "biological, therapeutic, or clinical decisions.",
            styles["Body"],
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "MOLE-AI v2 — Computational drug discovery and "
            "molecular prioritization",
            styles["Small"],
        )
    )

    document.build(story)

    return buffer.getvalue()
