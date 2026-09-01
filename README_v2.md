# 🧬 MOLE-AI

<p align="center">
  <img src="assets/images/logo.png" alt="MOLE-AI Logo" width="180">
</p>

<h1 align="center">MOLE-AI</h1>

<h3 align="center">
AI-Powered Molecular Property Prediction & Computational Drug Discovery Platform
</h3>

<p align="center">
An integrated cheminformatics and AI platform for molecular analysis,
property prediction, candidate prioritization, optimization, and
computational drug discovery.
</p>

---
## 🚀 MOLE-AI v2.0.0

**MOLE-AI v2** is the next-generation version of the MOLE-AI platform, designed to support an end-to-end computational workflow for molecular analysis and AI-assisted drug discovery.

Building on the original MOLE-AI toolkit, v2 integrates molecular analysis, QSAR prediction, ADMET assessment, molecular similarity, candidate ranking, molecular generation, molecular optimization, and batch screening into a unified interactive platform.

The goal of MOLE-AI v2 is to help researchers **analyze molecules, prioritize computational candidates, explore chemical space, and generate reproducible computational reports** through an accessible AI-driven workflow.

### What is new in v2?

Compared with the original MOLE-AI release, v2 introduces a more integrated drug-discovery workflow with:

- 🧬 Individual molecular analysis
- 🧠 AI-based QSAR prediction
- 💊 ADMET and drug-likeness assessment
- 🎯 Multi-criteria candidate ranking
- 🧪 Molecular generation
- ⚗️ Molecular optimization
- 🔬 Molecular similarity analysis
- 📊 Batch molecular screening
- 📄 Professional PDF research reports
- 📥 CSV export of computational results
- 🔍 Candidate evaluation and prioritization

MOLE-AI v2 is intended as a **research and computational decision-support platform**, helping researchers move from individual molecular analysis toward systematic computational screening and candidate prioritization.

> **Important:** MOLE-AI v2 provides computational predictions and hypotheses. Results are not experimental validation and should be independently evaluated using appropriate chemical, biological, and experimental methods.

### 🌐 Live Application

**Try MOLE-AI online:**

https://mole-ai-toolkit.streamlit.app/

---

# 🔬 Key Features

## 1. Molecular Analysis

Analyze individual molecules directly from their SMILES representation.

* SMILES validation
* Molecular structure visualization
* Molecular descriptors
* Molecular properties
* Chemical feature analysis
* Comprehensive computational assessment

---

## 2. AI Molecular Property Prediction

MOLE-AI provides machine-learning-based molecular property prediction.

### QSAR

* Morgan fingerprint-based molecular representation
* Random Forest QSAR model
* Predicted pIC50
* Activity classification
* Candidate prioritization

> Predictions are computational estimates and should not be interpreted as experimental measurements.

---

## 3. ADMET Analysis

Evaluate computational ADMET-related molecular properties.

The platform provides:

* ADMET scoring
* Drug-likeness assessment
* Lipinski rule evaluation
* Molecular property analysis
* Computational candidate assessment

---

## 4. Candidate Ranking

MOLE-AI integrates molecular prediction outputs into a candidate-ranking workflow.

Candidates can be prioritized using:

* Predicted activity
* ADMET score
* Molecular properties
* Overall candidate score
* Priority classification

This allows researchers to move from individual predictions toward **computational candidate prioritization**.

---

## 5. Molecular Generation

MOLE-AI can generate computational molecular candidates using structural transformation strategies.

Generated candidates can subsequently be evaluated using the existing:

* QSAR prediction
* ADMET analysis
* Molecular similarity
* Candidate ranking

workflow.

> Generated molecules are computational hypotheses and require further chemical, biological, and experimental evaluation.

---

## 6. Molecular Optimization

The platform supports computational molecular optimization to explore candidate structures and prioritize potentially improved molecules.

The optimization workflow integrates molecular properties and predictive scores to support iterative candidate evaluation.

---

## 7. Molecular Similarity

Compare molecules using computational molecular fingerprints and similarity analysis.

This can support:

* Molecular similarity assessment
* Candidate comparison
* Structural prioritization
* Chemical library exploration

---

## 8. Batch Molecular Screening

MOLE-AI v2 supports screening multiple molecules in a single workflow.

The batch screening pipeline provides:

* Molecular validation
* Molecular property analysis
* Prediction
* Candidate ranking
* Screening analytics
* Ranked candidate tables
* CSV export
* Professional PDF reporting

This allows researchers to move from **single-molecule analysis to library-scale computational screening**.

---

## 9. Professional Research Reports

MOLE-AI v2 provides downloadable professional PDF reports for computational analysis.

### Individual molecule reports

Generate a structured PDF report containing molecular analysis and computational results.

### Batch screening reports

Generate a professional report summarizing ranked screening results.

Reports can be used for:

* Research documentation
* Candidate comparison
* Computational screening records
* Internal project reporting
* Further scientific evaluation

---

# 🧠 MOLE-AI v2 Workflow

```text
                    Molecular Input
                          │
                          ▼
                  SMILES Validation
                          │
                          ▼
                  Molecular Analysis
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
           QSAR         ADMET      Similarity
             │            │            │
             └────────────┼────────────┘
                          ▼
                  Candidate Ranking
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
       Molecular Generation     Optimization
              │                       │
              └───────────┬───────────┘
                          ▼
                  Candidate Evaluation
                          │
                          ▼
                 Batch Screening
                          │
                          ▼
              CSV / Professional PDF
```

---

# 🛠️ Technology Stack

* **Python 3.11+**
* **Streamlit**
* **RDKit**
* **NumPy**
* **Pandas**
* **Scikit-learn**
* **Plotly**
* **Matplotlib**
* **ReportLab**
* **Pytest**
* **Git / GitHub**

---

# 📦 Installation

Clone the repository:

```bash
git clone https://github.com/Mehwish55/MOLE-AI.git
cd MOLE-AI
```

Create and activate the environment:

```bash
conda create -n mole-ai-v2 python=3.11
conda activate mole-ai-v2
```

Install dependencies:

```bash
pip install -r requirements.txt
```

For RDKit system dependencies required by the Streamlit deployment environment, see:

```text
packages.txt
```

---

# ▶️ Run MOLE-AI Locally

Run the v2 application:

```bash
streamlit run v2_app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

# 🧪 Testing

MOLE-AI includes an automated test suite.

Run:

```bash
pytest -q
```

Current validation:

```text
74 passed
```

Python syntax can be checked with:

```bash
python -m py_compile v2_app.py
```

Dependency consistency can be checked with:

```bash
pip check
```

---

# 📊 Reproducibility

The main application dependencies are version-pinned to improve reproducibility.

Current validated environment:

```text
Python       3.11.15
Streamlit    1.59.2
NumPy        1.26.4
Pandas       3.0.5
Scikit-learn 1.9.0
RDKit        2022.9.5
Plotly       6.9.0
ReportLab    5.0.1
```

---

# ⚠️ Scientific Disclaimer

MOLE-AI is a **computational research and drug-discovery support platform**.

Predictions, rankings, generated molecules, ADMET scores, and other computational outputs are not experimental validation and should not be interpreted as confirmed biological activity, efficacy, toxicity, or clinical suitability.

All computational candidates require appropriate chemical, biological, experimental, and regulatory evaluation before any real-world application.

---

# 📁 Project Structure

```text
MOLE-AI/
│
├── assets/
│   └── images/
│       └── logo.png
│
├── data/
│
├── docs/
│
├── mole_ai/
│   ├── agents/
│   ├── chem/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── ranking/
│   ├── reports/
│   ├── utils/
│   └── workflows/
│
├── tests/
│
├── v2_app.py
├── app.py
├── requirements.txt
├── packages.txt
├── environment.yml
├── pyproject.toml
├── CHANGELOG.md
├── RELEASE_NOTES.md
├── LICENSE
└── README.md
```

---

# 📜 License

MOLE-AI is released under the MIT License.

See [LICENSE](LICENSE) for details.

---

# 🔭 Future Development

Potential future directions include:

* Advanced QSAR models
* Deep-learning molecular models
* Graph neural networks
* Transformer-based molecular modeling
* Molecular docking integration
* Larger chemical-library screening
* Improved uncertainty estimation
* Explainable AI for molecular predictions
* Additional ADMET endpoints
* Experimental validation workflows
* Research and industry integration

---

# 👩‍🔬 Author

**Mehwish Shafiq**

Biotechnology & Bioinformatics Researcher

MOLE-AI is developed as an open-source computational research platform for AI-assisted molecular analysis and drug discovery.

---

## ⭐ Project Status

**MOLE-AI v2.0.0 — Release Candidate**

The v2 platform has been validated with automated testing and is being prepared for public deployment.

Computational predictions should be independently validated before scientific or experimental use.

