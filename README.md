# 🧬 MOLE-AI

### An Open-Source Toolkit for Multi-Objective AI Drug Design

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Release](https://img.shields.io/badge/Release-v1.0.0-blue.svg)]()
[![Status](https://img.shields.io/badge/Status-Stable-green.svg)]()

MOLE-AI is an open-source AI-driven drug discovery toolkit that combines
machine learning, deep learning, and computational chemistry to support
molecular property prediction, molecular analysis, generation, optimization,
ADMET prediction, docking utilities, and candidate ranking.

---

# 📌 Current Status

## MOLE-AI v1.0.0 — First Stable Release

The current implementation includes:

- ✅ RDKit molecular preprocessing
- ✅ SMILES validation
- ✅ Molecular descriptor calculation
- ✅ Morgan fingerprint generation
- ✅ ChEMBL dataset preprocessing
- ✅ Feature engineering pipeline
- ✅ QSAR model training
- ✅ Random Forest QSAR prediction
- ✅ Model evaluation (MAE, RMSE, R²)
- ✅ Batch prediction
- ✅ Prediction reporting
- ✅ Molecular similarity search
- ✅ Dataset management
- ✅ Model registry utilities
- ✅ Experiment tracking utilities
- ✅ Deep learning QSAR models
- ✅ Graph neural network foundation
- ✅ Transformer molecular models
- ✅ ADMET prediction utilities
- ✅ Molecular generation utilities
- ✅ Molecular optimization
- ✅ Docking integration utilities
- ✅ Streamlit web interface
- ✅ Automated testing with pytest

---

# 🚀 Features

## Chemistry Processing

- SMILES validation
- RDKit molecular conversion
- Descriptor calculation
- Fingerprint generation
- Molecular similarity analysis

## Machine Learning

- QSAR regression models
- Random Forest prediction
- Model evaluation
- Batch prediction
- Prediction reports

## Deep Learning

- Feed-forward QSAR neural networks
- Molecular graph neural network foundation
- Transformer molecular models

## Drug Discovery Utilities

- ADMET prediction
- Molecular generation
- Molecular optimization
- Docking result processing
- Candidate ranking

## User Interface

- Interactive Streamlit application
- Molecular prediction interface
- User-friendly workflow

---

# 🔬 Workflow
Input Molecule / Target
│
▼
SMILES Processing
│
▼
Molecular Features
│
▼
QSAR Prediction
│
▼
Deep Learning Models
│
▼
ADMET Analysis
│
▼
Molecular Similarity
│
▼
Molecular Optimization
│
▼
Docking Evaluation
│
▼
Candidate Ranking
│
▼
Prediction Report

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Mehwish55/MOLE-AI.git

cd MOLE-AI

Create environment:
conda create -n mole-ai python=3.11

conda activate mole-ai

Install dependencies:
pip install -r requirements.txt

Example Usage
Python API

from mole_ai import Predictor

predictor = Predictor()

result = predictor.predict(
    smiles="CCO"
)

print(result)

Web Interface

MOLE-AI includes an interactive Streamlit interface.

Launch:
streamlit run mole_ai/app.py

Open your browser:
http://localhost:8501

The interface provides:

Molecular property prediction
Interactive molecular analysis
Prediction results
User-friendly workflow

# 🌐 Web Interface

MOLE-AI provides an interactive Streamlit-based web interface for molecular
property prediction and analysis.

## Launch the Application

Activate the MOLE-AI environment:

```bash
conda activate mole-ai
Start the Streamlit application:

streamlit run mole_ai/app.py

Open the application in your browser:

http://localhost:8501
Example Workflow
Enter a molecular SMILES string.

Example:

CCO
Submit the molecule for prediction.
The interface returns molecular property predictions.

The web interface provides:

Molecular input through SMILES
QSAR prediction
Prediction results
Interactive molecular analysis
User-friendly visualization workflow
🧪 Running Tests

MOLE-AI uses pytest for automated testing.

Run the complete test suite:

pytest -v

Run individual test modules:

pytest tests/test_predict.py -v

Example:

pytest tests/test_models.py -v

All implemented modules are validated through automated unit tests.

📂 Project Structure
MOLE-AI/

├── mole_ai/
│   │
│   ├── chem/
│   │   ├── smiles.py
│   │   ├── descriptors.py
│   │   └── fingerprints.py
│   │
│   ├── features/
│   │   └── feature engineering modules
│   │
│   ├── models/
│   │   ├── train.py
│   │   ├── predict.py
│   │   ├── evaluate.py
│   │   ├── deep_learning.py
│   │   ├── graph_neural_network.py
│   │   ├── transformer.py
│   │   ├── admet.py
│   │   ├── optimization.py
│   │   └── docking.py
│   │
│   ├── app.py
│   └── cli.py
│
├── data/
│
├── examples/
│
├── notebooks/
│
├── docs/
│   ├── index.md
│   ├── user_guide.md
│   ├── workflow.md
│   └── api.md
│
├── tests/
│
├── requirements.txt
│
└── README.md
🗺️ Future Roadmap

Future development directions include:

 Large-scale pretrained molecular foundation models
 Advanced graph neural network architectures
 Transformer model fine-tuning
 Real-time docking integration
 Cloud-based deployment
 Advanced molecular visualization dashboard
 Larger chemical database integration
 Automated model benchmarking platform
 Improved explainable AI modules
🛠 Technologies

MOLE-AI is built using modern computational chemistry and machine learning
technologies.

Programming
Python 3.11+
Chemistry
RDKit
ChEMBL
PubChem
Protein Data Bank (PDB)
Machine Learning
Scikit-learn
PyTorch
PyTorch Geometric
AI and Deep Learning
Neural Networks
Graph Neural Networks
Transformer architectures
Applications
Streamlit
AutoDock Vina
GROMACS
📚 Datasets

MOLE-AI supports molecular datasets including:

ChEMBL
PubChem
Protein Data Bank (PDB)

These resources enable:

Molecular property prediction
QSAR modelling
Molecular optimization
Drug discovery workflows
💻 Command-Line Interface

MOLE-AI provides command-line utilities.

Display Version
python -m mole_ai.cli --version
Run Prediction
python -m mole_ai.cli \
    --predict \
    --model models/model.pkl \
    --input data/features.csv \
    --output predictions.csv

The CLI supports automated prediction workflows and integration into
computational pipelines.

📖 Documentation

Complete documentation is available in the docs directory.

docs/

├── index.md
├── user_guide.md
├── workflow.md
└── api.md

Documentation includes:

Installation guide
User workflow
API reference
Pipeline explanations
📦 Release
MOLE-AI v1.0.0

First stable release.

Included capabilities:

Molecular preprocessing
Descriptor generation
Fingerprint generation
QSAR prediction
Deep learning models
Molecular similarity analysis
ADMET prediction utilities
Molecular generation
Molecular optimization
Docking utilities
Streamlit interface
Citation

If you use MOLE-AI in academic research, please cite this repository.

Citation information will be updated with future academic publications.

Contributing

Contributions are welcome.

To contribute:

Fork the repository
Create a feature branch
git checkout -b feature/new-feature
Add implementation and tests
Run the test suite
pytest -v
Submit a pull request
License

MIT License

MOLE-AI is free to use, modify, and distribute according to the MIT License.

Contact

GitHub Issues are the preferred way to:

Report bugs
Request new features
Discuss improvements
Suggest ideas
🧬 MOLE-AI v1.0.0

An open-source toolkit combining artificial intelligence,
machine learning, and computational chemistry for modern drug discovery.
