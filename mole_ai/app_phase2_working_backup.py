"""
Streamlit web interface for MOLE-AI.
"""

import streamlit as st
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import Lipinski
from rdkit.Chem import Draw

from rdkit.Chem import rdMolDescriptors
from mole_ai.chem.smiles import validate_smiles
from mole_ai.chem.fingerprints import (
    generate_morgan_fingerprint
)
import pandas as pd

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

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🧪 Molecular Analysis",
        "🧬 Fingerprint Generation",
        "🤖 AI Prediction",
        "📚 About MOLE-AI"
    ]
)
# ==========================
# Tab 1
# ==========================

with tab1:

    st.subheader("🧪 Molecular Analysis")

    smiles = st.text_input(
        "Enter SMILES molecule",
        placeholder="Example: CCO"
    )

    st.markdown("### 🧪 Example Molecules")

    example_molecules = {
        "Ethanol": "CCO",
        "Aspirin": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "Caffeine": "Cn1cnc2n(C)c(=O)n(C)c(=O)c12",
        "Paracetamol": "CC(=O)NC1=CC=C(C=C1)O",
        "Ibuprofen": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"
    }

    st.write("Copy an example SMILES:")

    for name, smiles_example in example_molecules.items():
        st.code(f"{name}: {smiles_example}")

    if st.button("🔬 Analyze Molecule"):

        if validate_smiles(smiles):

            mol = Chem.MolFromSmiles(smiles)

            properties = get_molecular_properties(mol)

            st.success("🟢 Valid Molecule")

            left, right = st.columns([1,1])

            with left:

                st.subheader("🧬 Molecular Structure")

                image = Draw.MolToImage(
                    mol,
                    size=(450,450)
                )

                st.image(image)

            with right:

                st.subheader("📊 Molecular Properties")

                st.metric(
                    "Formula",
                    properties["Formula"]
                )

                st.metric(
                    "Molecular Weight",
                    properties["Molecular Weight"]
                )

                st.metric(
                    "Exact Weight",
                    properties["Exact Molecular Weight"]
                )

                st.metric(
                    "LogP",
                    properties["LogP"]
                )

                st.metric(
                    "TPSA",
                    properties["TPSA"]
                )

                st.metric(
                    "Heavy Atoms",
                    properties["Heavy Atoms"]
                )

                st.metric(
                    "H-Bond Donors",
                    properties["Hydrogen Bond Donors"]
                )

                st.metric(
                    "H-Bond Acceptors",
                    properties["Hydrogen Bond Acceptors"]
                )

                st.metric(
                    "Rotatable Bonds",
                    properties["Rotatable Bonds"]
                )

                st.metric(
                    "Ring Count",
                    properties["Ring Count"]
                )

            st.divider()

            mw = properties["Molecular Weight"]
            logp = properties["LogP"]
            hbd = properties["Hydrogen Bond Donors"]
            hba = properties["Hydrogen Bond Acceptors"]

            if (
                mw <= 500 and
                logp <= 5 and
                hbd <= 5 and
                hba <= 10
            ):

                st.success(
                    "💊 Lipinski Rule: PASS"
                )

            else:

                st.warning(
                    "⚠️ Lipinski Rule: FAIL"
                )

            with st.expander(
                "🔬 Advanced Molecular Descriptors"
            ):

                st.table(properties)

            st.subheader("📄 Molecular Summary")

            st.info(
                f"""
Formula: {properties['Formula']}

Molecular Weight: {properties['Molecular Weight']}

LogP: {properties['LogP']}

TPSA: {properties['TPSA']}

Status: Ready for AI Prediction 🚀
"""
            )

            st.divider()

            st.subheader("📥 Download Analysis")

            df = pd.DataFrame(
                list(properties.items()),
                columns=["Property", "Value"]
            )

            csv = df.to_csv(index=False)

            st.download_button(
                label="📥 Download CSV Report",
                data=csv,
                file_name="molecule_analysis.csv",
                mime="text/csv"

            )

        else:

            st.error(
                "❌ Invalid SMILES"
            )


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
# ==========================
# ==========================
# AI Prediction Tab
# ==========================

with tab3:

    st.subheader(
        "🤖 AI Molecular Property Prediction"
    )


    st.write(
        """
        MOLE-AI uses machine learning models
        to predict molecular properties.

        Planned prediction modules:

        ✓ QSAR activity prediction

        ✓ Molecular property prediction

        ✓ Drug candidate scoring

        ✓ Model-based ranking
        """
    )


    prediction_smiles = st.text_input(
        "Enter SMILES for prediction",
        placeholder="Example: CCO",
        key="prediction_input"
    )


    model_option = st.selectbox(
        "Select Prediction Model",
        [
            "Random Forest (QSAR)",
            "Deep Learning Model",
            "Graph Neural Network",
            "Transformer Model"
        ]
    )


    if st.button(
        "🚀 Predict Molecular Property"
    ):

        if prediction_smiles:

            mol = Chem.MolFromSmiles(
                prediction_smiles
            )


            if mol:

                st.success(
                    "✅ Molecule ready for prediction"
                )


                st.info(
                    f"""
                    Selected Model:

                    {model_option}


                    Prediction engine will be connected
                    with trained MOLE-AI models.
                    """
                )


            else:

                st.error(
                    "❌ Invalid SMILES"
                )

        else:

            st.warning(
                "Please enter a SMILES sequence"
            )
