from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import Crippen
from rdkit.Chem import Lipinski
from rdkit.Chem import rdMolDescriptors


def calculate_admet(smiles):

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None


    properties = {

        "Molecular Weight":
            round(Descriptors.MolWt(mol),2),

        "LogP":
            round(Crippen.MolLogP(mol),2),

        "H Bond Donors":
            Lipinski.NumHDonors(mol),

        "H Bond Acceptors":
            Lipinski.NumHAcceptors(mol),

        "Rotatable Bonds":
            Lipinski.NumRotatableBonds(mol),

        "TPSA":
            round(rdMolDescriptors.CalcTPSA(mol),2),

        "Aromatic Rings":
            Lipinski.NumAromaticRings(mol)

    }


    return properties



def lipinski_check(properties):

    violations = 0


    if properties["Molecular Weight"] > 500:
        violations += 1

    if properties["LogP"] > 5:
        violations += 1

    if properties["H Bond Donors"] > 5:
        violations += 1

    if properties["H Bond Acceptors"] > 10:
        violations += 1


    if violations == 0:
        return "Drug-like molecule ✅"

    else:
        return f"{violations} Lipinski violation(s) ⚠️"

def admet_score(properties):

    score = 100

    if properties["Molecular Weight"] > 500:
        score -= 20

    if properties["LogP"] > 5:
        score -= 20

    if properties["H Bond Donors"] > 5:
        score -= 10

    if properties["H Bond Acceptors"] > 10:
        score -= 10

    if properties["TPSA"] > 140:
        score -= 15

    return max(score, 0)
