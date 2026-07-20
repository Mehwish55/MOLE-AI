"""
Streamlit web interface for MOLE-AI.
"""

import streamlit as st

from mole_ai.chem.smiles import validate_smiles


st.title("MOLE-AI Drug Discovery Platform")

st.write(
    "Molecular prediction and analysis interface."
)


smiles = st.text_input(
    "Enter SMILES molecule",
)


if st.button("Analyze Molecule"):

    if validate_smiles(smiles):

        st.success(
            "Valid molecule detected"
        )

        st.write(
            "SMILES:",
            smiles,
        )

    else:

        st.error(
            "Invalid SMILES"
        )
