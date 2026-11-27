// Base URL of the MOLE-AI API (FastAPI service in api/).
// Local development uses the API on port 8000; set the deployed URL below.
window.MOLE_API =
  location.hostname === "localhost" || location.hostname === "127.0.0.1"
    ? "http://localhost:8000"
    : "https://mole-ai-api.onrender.com";
