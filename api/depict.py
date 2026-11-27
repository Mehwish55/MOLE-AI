"""2D structure depiction in the MOLE-AI house style (fine ink lines)."""

from __future__ import annotations

from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D

INK = (0.106, 0.114, 0.122)
PALETTE = {
    -1: INK,                     # default
    6: INK,                      # C
    1: INK,                      # H
    7: (0.122, 0.306, 0.239),    # N  — accent green
    8: (0.545, 0.180, 0.180),    # O  — oxblood
    9: (0.420, 0.420, 0.300),    # F
    15: (0.541, 0.353, 0.071),   # P
    16: (0.541, 0.353, 0.071),   # S  — amber
    17: (0.300, 0.420, 0.300),   # Cl
    35: (0.470, 0.250, 0.150),   # Br
}


def mol_svg(smiles: str, width: int = 360, height: int = 260, line: float = 1.6) -> str | None:
    """Return an SVG string for ``smiles`` or ``None`` if it cannot be parsed."""
    mol = Chem.MolFromSmiles(smiles) if smiles else None
    if mol is None:
        return None
    drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
    opts = drawer.drawOptions()
    opts.clearBackground = False
    opts.bondLineWidth = line
    opts.scaleBondWidth = False
    opts.padding = 0.08
    opts.multipleBondOffset = 0.18
    opts.additionalAtomLabelPadding = 0.12
    opts.minFontSize = 11
    opts.updateAtomPalette(PALETTE)
    rdMolDraw2D.PrepareAndDrawMolecule(drawer, mol)
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()
    # Strip the XML prolog so the markup can be inlined in HTML.
    return svg[svg.find("<svg"):]
