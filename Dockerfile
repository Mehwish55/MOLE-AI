# syntax=docker/dockerfile:1
FROM python:3.11-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libxrender1 \
    libxext6 \
    libsm6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD curl --fail "http://localhost:${PORT:-8501}/_stcore/health" || exit 1

CMD ["sh", "-c", "streamlit run v2_app.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.headless=true"]
