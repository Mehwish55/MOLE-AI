"""Vercel serverless entrypoint for the MOLE-AI API.

Vercel routes ``/api/*`` here; the FastAPI app in ``api/main.py`` defines its
routes without that prefix, so it is stripped before the request reaches it.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from api.main import app as _api  # noqa: E402


async def app(scope, receive, send):
    if scope["type"] in ("http", "websocket"):
        path = scope.get("path", "")
        if path == "/api" or path.startswith("/api/"):
            scope = dict(scope)
            scope["path"] = path[4:] or "/"
            raw = scope.get("raw_path")
            if raw and raw.startswith(b"/api"):
                scope["raw_path"] = raw[4:] or b"/"
    await _api(scope, receive, send)
