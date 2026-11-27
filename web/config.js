// Base URL of the MOLE-AI API (FastAPI service in api/).
// Locally the API runs on port 8000; on Vercel it is served from /api on the
// same domain (see vercel.json and vercel_api/index.py).
window.MOLE_API =
  location.hostname === "localhost" || location.hostname === "127.0.0.1"
    ? "http://localhost:8000"
    : "/api";
