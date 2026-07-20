# MOLE-AI API Documentation

## Chemistry Module

### SMILES Processing

Module:

```python
mole_ai.chem.smiles
```

## Functions

### smiles_to_mol()

Convert a SMILES string into an RDKit molecule.

Example:

```python
from mole_ai.chem.smiles import smiles_to_mol

mol = smiles_to_mol("CCO")
```

Returns:

```text
RDKit molecule object or None
```

---

### validate_smiles()

Validate a SMILES string.

Example:

```python
from mole_ai.chem.smiles import validate_smiles

valid = validate_smiles("CCO")

print(valid)
```

Output:

```text
True
```

Invalid example:

```python
validate_smiles("INVALID")
```

Output:

```text
False
```
