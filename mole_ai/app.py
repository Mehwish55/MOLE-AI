"""
Streamlit web interface for MOLE-AI.
"""

import streamlit as st
from pathlib import Path
from datetime import datetime

from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import Lipinski
from rdkit.Chem import Draw

from rdkit.Chem import rdMolDescriptors
from mole_ai.chem.smiles import validate_smiles
from mole_ai.chem.fingerprints import (
    generate_morgan_fingerprint
)
from mole_ai.chem.descriptors import get_molecular_properties
from mole_ai.models.predict import (
    predict_from_smiles
)
from mole_ai.admet import calculate_admet, lipinski_check, admet_score
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

if "prediction_history" not in st.session_state:

    st.session_state.prediction_history = []

# ==========================
# MOLE-AI Logo Header
# ==========================

logo_path = Path(
    "assets/images/logo.png"
)


if logo_path.exists():

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        st.image(
            str(logo_path),
            width=350
        )


# Space

st.write("")


# ==========================
# Full Width Banner
# ==========================

banner_path = Path(
    "assets/images/banner.png"
)


if banner_path.exists():

    st.image(
        str(banner_path),
        use_container_width=True
    )


# Space

st.write("")


# ==========================
# Title
# ==========================

st.markdown(
"""
<h1 style="text-align:center;">
🧬 MOLE-AI
</h1>

<h3 style="text-align:center;">
AI-Powered Molecular Intelligence Platform
</h3>

<p style="text-align:center;">
Computational Drug Discovery |
Machine Learning |
Cheminformatics
</p>

""",
unsafe_allow_html=True
)


# ==========================
# Sidebar
# ==========================

st.sidebar.title("🧬 MOLE-AI")

st.sidebar.info(
    """
    Platform Features:

    ✓ SMILES Validation

    ✓ Molecular Analysis

    ✓ Molecular Descriptors

    ✓ QSAR Prediction

    ✓ AI Drug Discovery Workflow
    """
)


# ==========================
# Molecular Input
# =========================

# ==========================
# Application Tabs
# ==========================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🧪 Molecular Analysis",
        "🧬 Fingerprint Generation",
        "🤖 AI Prediction",
        "💊 ADMET Analysis",
        "📚 About MOLE-AI"
    ]
)

# ==========================
# Tab 1
# ==========================
with tab1:

    st.subheader("🧪 Molecular Analysis")

    st.success("Tab loaded successfully!")

    smiles = st.text_input(
        "Enter SMILES molecule",
        value="CCO"
    )

    st.write("Current SMILES:")
    st.write(smiles)

if st.button("🔬 Analyze Molecule"):

    st.write("STEP 1")

    mol = Chem.MolFromSmiles(smiles)

    st.write("STEP 2")

    if mol is not None:
        st.success("Valid molecule")

        image = Draw.MolToImage(
            mol,
            size=(450,450)
        )

        st.image(image)

    else:
        st.error("Invalid SMILES")

# ==========================
# Tab 2
# ==========================

# ==========================
# Fingerprint Tab
# ==========================

with tab2:

    st.subheader(
        "🧬 Molecular Fingerprint Generation"
    )


    fp_smiles = st.text_input(
        "Enter SMILES for fingerprint",
        placeholder="Example: CCO",
        key="fingerprint_input"
    )


    if st.button(
        "Generate Fingerprint"
    ):

        mol = Chem.MolFromSmiles(fp_smiles)


        if mol:

            fingerprint = generate_morgan_fingerprint(
                mol
            )


            st.success(
                "✅ Morgan fingerprint generated"
            )


            st.write(
                "Fingerprint size:",
                len(fingerprint)
            )


            bits = list(
                fingerprint.GetOnBits()
            )


            st.write(
                "Active fingerprint bits:"
            )

            st.write(bits)


        else:

            st.error(
                "❌ Invalid SMILES"
            )
# ==========================
# Tab 3
# AI Prediction Tab
# ==========================

with tab3:

    st.subheader(
        "🤖 AI Molecular Activity Prediction"
    )

    st.info(
        """
        MOLE-AI QSAR Engine

        Model:
        Random Forest Regression

        Features:
        Morgan Fingerprints (2048 bits)

        Output:
        Predicted molecular activity (pIC50)
        """
    )


    prediction_smiles = st.text_input(
        "Enter SMILES molecule",
        placeholder="Example: CCO",
        key="prediction_input"
    )


    if st.button(
        "🚀 Predict pIC50",
        key="prediction_button"
    ):

        if prediction_smiles:

            prediction = predict_from_smiles(
                prediction_smiles
            )


            if prediction is not None:


                st.success(
                    "✅ Prediction completed successfully"
                )


                st.session_state.prediction_history.append(
                    {
                        "SMILES": prediction_smiles,
                        "Predicted pIC50": round(
                            prediction,
                            3
                        )
                    }
                )


                st.divider()


                col1, col2 = st.columns(
                    2
                )


                with col1:

                    st.subheader(
                        "🧬 Molecular Structure"
                    )


                    mol = Chem.MolFromSmiles(
                        prediction_smiles
                    )


                    if mol:

                        image = Draw.MolToImage(
                            mol,
                            size=(350,350)
                        )

                        st.image(
                            image,
                            caption="2D Structure"
                        )


                with col2:

                    st.subheader(
                        "🤖 Prediction Result"
                    )


                    st.metric(
                        "Predicted pIC50",
                        f"{prediction:.3f}"
                    )


                    if prediction >= 7:

                        activity = "High Activity"

                        score = 90


                    elif prediction >= 5:

                        activity = "Moderate Activity"

                        score = 70


                    else:

                        activity = "Low Activity"

                        score = 40



                    st.write(
                        "### Activity Classification"
                    )


                    st.success(
                        activity
                    )


                    st.progress(
                        score / 100
                    )


                    st.write(
                        f"Candidate Score: {score}%"
                    )



                st.divider()


                st.subheader(
                    "🧪 Molecular Properties"
                )


                mol = Chem.MolFromSmiles(
                    prediction_smiles
                )


                if mol:

                    properties = get_molecular_properties(
                        mol
                    )

                    st.table(
                        properties
                    )



                st.divider()


                st.subheader(
                    "📜 Prediction History"
                )


                history_df = pd.DataFrame(
                    st.session_state.prediction_history
                )


                st.dataframe(
                    history_df,
                    use_container_width=True
                )


                st.download_button(
                    "⬇️ Download Predictions",
                    history_df.to_csv(
                        index=False
                    ),
                    "mole_ai_predictions.csv",
                    "text/csv"
                )



                st.divider()


                st.subheader(
                    "🧠 AI Interpretation"
                )


                if prediction >= 7:

                    st.success(
                        """
                        This molecule shows strong predicted activity.

                        Recommended next steps:

                        ✓ Molecular docking

                        ✓ ADMET analysis

                        ✓ Toxicity evaluation

                        ✓ Experimental validation
                        """
                    )


                elif prediction >= 5:

                    st.info(
                        """
                        This molecule shows moderate predicted activity.

                        Optimization of molecular properties may improve performance.
                        """
                    )


                else:

                    st.warning(
                        """
                        This molecule shows lower predicted activity.

                        Structural optimization may be required.
                        """
                    )


            else:

                st.error(
                    "❌ Invalid SMILES or prediction failed"
                )


        else:

            st.warning(
                "Please enter a SMILES molecule"
            )

# ==========================
# Tab 4
# ADMET ANALYSIS
# =========================
with tab4:

    st.header("💊 ADMET Analysis")

    st.write(
        """
        Evaluate molecular absorption, distribution, metabolism,
        excretion, and toxicity (ADMET) properties using
        molecular descriptors and drug-likeness rules.
        """
    )


    smiles_admet = st.text_input(
        "Enter SMILES for ADMET analysis",
        value="CC(=O)OC1=CC=CC=C1C(=O)O"
    )


    if st.button("Analyze ADMET"):


        results = calculate_admet(smiles_admet)


        if results:


            st.subheader("🧬 Molecular Properties")


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Molecular Weight",
                    f"{results['Molecular Weight']} Da"
                )

                st.metric(
                    "LogP",
                    results["LogP"]
                )


            with col2:

                st.metric(
                    "H Bond Donors",
                    results["H Bond Donors"]
                )

                st.metric(
                    "H Bond Acceptors",
                    results["H Bond Acceptors"]
                )


            with col3:

                st.metric(
                    "TPSA",
                    results["TPSA"]
                )

                st.metric(
                    "Aromatic Rings",
                    results["Aromatic Rings"]
                )


            st.divider()


            st.subheader("💊 ADMET Drug-likeness Score")


            score = admet_score(results)


            st.metric(
                "Overall ADMET Score",
                f"{score}/100"
            )


            if score >= 80:

                st.success(
                    "Excellent drug-like profile ✅"
                )


            elif score >= 60:

                st.warning(
                    "Moderate drug-like profile ⚠️"
                )


            else:

                st.error(
                    "Poor drug-like profile ❌"
                )


            st.divider()


            st.subheader("📋 Lipinski Rule of Five")


            st.info(
                lipinski_check(results)
            )


            st.divider()


            st.subheader("🧠 AI Interpretation")


            if score >= 80:

                st.write(
                    """
                    This molecule shows favorable ADMET characteristics.

                    ✔ Suitable molecular weight
                    ✔ Acceptable lipophilicity
                    ✔ Good hydrogen bonding properties

                    Recommendation:
                    Candidate for further experimental validation.
                    """
                )


            elif score >= 60:

                st.write(
                    """
                    This molecule has acceptable properties,
                    but optimization may improve drug potential.
                    """
                )


            else:

                st.write(
                    """
                    This molecule shows unfavorable ADMET
                    characteristics and may require optimization.
                    """
                )
            st.divider()

            st.subheader("📄 Download ADMET Report")


            report = f"""
MOLE-AI Drug Discovery Report
============================

Generated:
{datetime.now()}


SMILES:
{smiles_admet}


Molecular Properties
--------------------

Molecular Weight:
{results['Molecular Weight']} Da

LogP:
{results['LogP']}

H Bond Donors:
{results['H Bond Donors']}

H Bond Acceptors:
{results['H Bond Acceptors']}

TPSA:
{results['TPSA']}

Aromatic Rings:
{results['Aromatic Rings']}


Lipinski Rule of Five
---------------------

{lipinski_check(results)}


ADMET Score
-----------

{score}/100


AI Interpretation
-----------------

"""


            if score >= 80:

                report += """
Excellent drug-like profile.

The molecule shows favorable physicochemical
properties and may be suitable for further
experimental validation.
"""


            elif score >= 60:

                report += """
Moderate drug-like profile.

Optimization may improve drug potential.
"""


            else:

                report += """
Poor drug-like profile.

Structural optimization may be required.
"""


            st.download_button(
                label="⬇️ Download ADMET Report",
                data=report,
                file_name="MOLE_AI_ADMET_Report.txt",
                mime="text/plain"
            )


            st.divider()


            st.subheader("📊 ADMET Property Profile")


            admet_values = {

                "Molecular Weight":
                    results["Molecular Weight"],

                "LogP":
                    results["LogP"],

                "HBD":
                    results["H Bond Donors"],

                "HBA":
                    results["H Bond Acceptors"],

                "TPSA":
                    results["TPSA"],

                "Aromatic Rings":
                    results["Aromatic Rings"]

            }


            fig, ax = plt.subplots(
                figsize=(8,4)
            )


            ax.bar(
                admet_values.keys(),
                admet_values.values()
            )


            ax.set_ylabel(
                "Value"
            )


            ax.set_title(
                "Molecular ADMET Properties"
            )


            plt.xticks(
                rotation=45,
                ha="right"
            )


            st.pyplot(fig)


        else:

            st.error(
                "Invalid SMILES. Please enter a valid molecular structure."
            )

# ==========================
# Tab 5
# About MOLE-AI
# ==========================

with tab5:

    st.subheader(
        "📚 About MOLE-AI"
    )


    st.markdown(
        """
# 🧬 MOLE-AI

**An open-source AI-powered molecular intelligence toolkit
for computational drug discovery.**

MOLE-AI combines molecular informatics,
machine learning, and cheminformatics to support
early-stage drug discovery workflows.
        """
    )


    st.divider()


    st.subheader(
        "🚀 AI Drug Discovery Workflow"
    )


    st.code(
        """
SMILES Input
      |
      ↓
RDKit Molecular Processing
      |
      ↓
Morgan Fingerprint Generation
      |
      ↓
Random Forest QSAR Model
      |
      ↓
pIC50 Activity Prediction
      |
      ↓
Candidate Prioritization
        """
    )


    st.divider()


    st.subheader(
        "✨ Core Features"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.info(
            """
🧪 Molecular Analysis

• Molecular descriptors

• Lipinski properties

• Drug-like evaluation
            """
        )


        st.success(
            """
🧬 Fingerprint Generation

• Morgan fingerprints

• 2048-bit molecular features
            """
        )


    with col2:

        st.warning(
            """
🤖 QSAR Prediction

• Random Forest regression

• pIC50 prediction
            """
        )


        st.success(
            """
📊 Machine Learning Stack

• Python

• RDKit

• Scikit-learn

• Streamlit
            """
        )


    st.divider()


    st.subheader(
        "🛠 Technology Stack"
    )


    st.table(
        {
            "Component": [
                "Programming",
                "Chemistry",
                "Machine Learning",
                "Data Processing",
                "Interface"
            ],

            "Technology": [
                "Python",
                "RDKit",
                "Scikit-learn",
                "Pandas / NumPy",
                "Streamlit"
            ]
        }
    )


    st.divider()


    st.subheader(
        "🗺 Development Roadmap"
    )


    st.markdown(
        """
### Version 1.0 ✅

✓ Molecular Analysis

✓ Fingerprint Generation

✓ QSAR Prediction


### Version 2.0 🚀

○ ADMET Prediction

○ Toxicity Prediction

○ Molecular Docking


### Version 3.0 🔬

○ Deep Learning Models

○ Generative AI Molecule Design

○ Multi-objective Optimization
        """
    )


    st.divider()


    st.subheader(
        "👩‍🔬 Project Information"
    )


    st.markdown(
        """
**MOLE-AI v1.0.0**

AI-powered molecular intelligence platform.

Built with:

Python | RDKit | Machine Learning | Streamlit

Designed for computational drug discovery research.
        """
    )

# ==========================
# Footer
# ==========================

st.divider()

st.markdown(
"""
<center>

🧬 <b>MOLE-AI v1.0.0</b><br>

AI-powered molecular intelligence platform<br>

Built with Python | RDKit | Streamlit | Machine Learning

</center>
""",
unsafe_allow_html=True
)
