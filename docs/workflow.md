# MOLE-AI Workflow

The current MOLE-AI pipeline consists of the following steps:

```text
SMILES
   │
   ▼
RDKit Processing
   │
   ▼
Descriptor Calculation
   │
   ▼
Morgan Fingerprints
   │
   ▼
Feature Matrix
   │
   ▼
Random Forest Training
   │
   ▼
Model Evaluation
   │
   ▼
Prediction
```

Future versions will extend this workflow with:

- Graph Neural Networks
- Transformer models
- ADMET prediction
- Molecular docking
- Molecular generation
- Multi-objective optimization
