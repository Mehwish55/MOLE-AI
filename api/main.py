"""MOLE-AI HTTP API.

Thin FastAPI layer over the existing MOLE-AI workflows so any frontend
(e.g. the static site in ``web/``) can use them.
"""

from __future__ import annotations

import hmac
import io
import json
import math
import os
from typing import Any

import numpy as np
import pandas as pd
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field

from api.depict import mol_svg
from mole_ai.agents.similarity_agent import SimilarityAgent
from mole_ai.ranking.explanation import CandidateExplainer
from mole_ai.reports.pdf_report import (
    generate_batch_screening_report,
    generate_single_molecule_report,
)
from mole_ai.workflows.batch_screening import BatchScreeningWorkflow
from mole_ai.workflows.drug_discovery import DrugDiscoveryWorkflow

FREE_BATCH_LIMIT = 5
PAID_BATCH_LIMIT = 500
MAX_UPLOAD_BYTES = 5 * 1024 * 1024

app = FastAPI(title="MOLE-AI API", version="2.0")

_origins = [o.strip() for o in os.environ.get("ALLOWED_ORIGINS", "*").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ------------------------------------------------------------------ helpers


def _clean(value: Any) -> Any:
    """Make workflow output JSON-safe (numpy scalars, NaN, tuples...)."""
    if isinstance(value, dict):
        return {str(k): _clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_clean(v) for v in value]
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _frame_records(frame: pd.DataFrame) -> list[dict]:
    return _clean(frame.astype(object).where(pd.notna(frame), None).to_dict(orient="records"))


async def _read_csv(upload: UploadFile) -> pd.DataFrame:
    raw = await upload.read()
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "File is larger than 5 MB.")
    try:
        frame = pd.read_csv(io.BytesIO(raw))
    except Exception as error:  # noqa: BLE001
        raise HTTPException(400, f"Could not read CSV: {error}") from error
    frame.columns = [str(c).strip().lower() for c in frame.columns]
    if "smiles" not in frame.columns:
        raise HTTPException(400, "No 'smiles' column found in this file.")
    return frame


def _analyze(smiles: str) -> tuple[dict, dict]:
    smiles = smiles.strip()
    if not smiles:
        raise HTTPException(400, "Enter a SMILES string.")
    try:
        result = DrugDiscoveryWorkflow().analyze(smiles)
    except ValueError as error:
        raise HTTPException(422, f"That SMILES string could not be parsed. {error}") from error
    explanation = CandidateExplainer().explain(result)
    return result, explanation


def _check_access(code: str | None, count: int) -> None:
    if count > PAID_BATCH_LIMIT:
        raise HTTPException(
            413,
            f"This file has {count} molecules; the limit is {PAID_BATCH_LIMIT}.",
        )
    if count <= FREE_BATCH_LIMIT:
        return
    expected = os.environ.get("MOLE_AI_ACCESS_CODE", "")
    if not expected:
        raise HTTPException(402, "Paid access is not configured yet. Contact MOLE-AI.")
    if not code or not hmac.compare_digest(code.strip(), expected.strip()):
        raise HTTPException(
            402,
            f"{count} molecules requires a paid batch (€49). Enter a valid access code.",
        )


def _pdf(data: bytes, name: str) -> Response:
    return Response(
        content=bytes(data),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )


# ------------------------------------------------------------------ routes


class AnalyzeRequest(BaseModel):
    smiles: str = Field(..., max_length=2000)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "free_limit": FREE_BATCH_LIMIT, "paid_limit": PAID_BATCH_LIMIT}


@app.post("/analyze")
def analyze(body: AnalyzeRequest) -> dict:
    result, explanation = _analyze(body.smiles)
    smiles = body.smiles.strip()
    analogues = {
        c.get("candidate_id"): mol_svg(c.get("smiles", ""), 150, 110, 1.2)
        for c in (result.get("generated_candidate_evaluation") or [])[:20]
    }
    return {
        "smiles": smiles,
        "structure": mol_svg(smiles, 420, 300),
        "analogue_structures": analogues,
        "result": _clean(result),
        "explanation": _clean(explanation),
    }


@app.post("/analyze/report")
def analyze_report(body: AnalyzeRequest) -> Response:
    result, explanation = _analyze(body.smiles)
    return _pdf(generate_single_molecule_report(result, explanation), "MOLE_AI_single_molecule_report.pdf")


async def _run_batch(file: UploadFile, access_code: str | None) -> pd.DataFrame:
    library = await _read_csv(file)
    _check_access(access_code, len(library))
    return BatchScreeningWorkflow().screen(library, smiles_column="smiles")


@app.post("/batch")
async def batch(file: UploadFile = File(...), access_code: str | None = Form(None)) -> dict:
    results = await _run_batch(file, access_code)
    return {"rows": _frame_records(results), "columns": list(results.columns)}


@app.post("/batch/report")
async def batch_report(file: UploadFile = File(...), access_code: str | None = Form(None)) -> Response:
    results = await _run_batch(file, access_code)
    return _pdf(generate_batch_screening_report(results), "MOLE_AI_batch_screening_report.pdf")


@app.post("/similarity")
async def similarity(
    file: UploadFile = File(...),
    query: str = Form(...),
    top_k: int = Form(10),
) -> dict:
    if not query.strip():
        raise HTTPException(400, "Enter a query SMILES.")
    library = await _read_csv(file)
    try:
        matches = SimilarityAgent().rank_similar(
            query.strip(),
            library.to_dict(orient="records"),
            top_k=max(1, min(int(top_k), 100)),
        )
    except ValueError as error:
        raise HTTPException(422, f"That query SMILES could not be parsed. {error}") from error
    matches = _clean(json.loads(json.dumps(matches, default=str)))
    for match in matches:
        match["structure"] = mol_svg(match.get("smiles", ""), 150, 110, 1.2)
    return {
        "library_size": len(library),
        "query_structure": mol_svg(query.strip(), 300, 220),
        "matches": matches,
    }
