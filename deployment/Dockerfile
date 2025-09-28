# --- Stage 1: Builder ---
FROM python:3.12-slim AS builder

# Install build essentials (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

# Copy production requirements only
COPY requirements_prod.txt ./requirements.txt

# Upgrade pip efficiently
RUN pip install --no-cache-dir --upgrade pip wheel

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies with optimization flags
RUN pip install --no-cache-dir \
    --disable-pip-version-check \
    --no-compile \
    -r requirements.txt \
    --extra-index-url https://download.pytorch.org/whl/cpu

# Pre-download your custom model (requires HF token)
ARG HF_TOKEN
RUN if [ -n "$HF_TOKEN" ]; then \
    python -c "\
    import os; \
    from transformers import AutoTokenizer, AutoModel; \
    from huggingface_hub import login; \
    login(token='$HF_TOKEN'); \
    os.makedirs('/opt/venv/model_cache', exist_ok=True); \
    os.environ['TRANSFORMERS_CACHE'] = '/opt/venv/model_cache'; \
    print('Downloading model...'); \
    tokenizer = AutoTokenizer.from_pretrained('hoangson2006/vietnamese-fraud-detection', cache_dir='/opt/venv/model_cache'); \
    model = AutoModel.from_pretrained('hoangson2006/vietnamese-fraud-detection', cache_dir='/opt/venv/model_cache'); \
    print('Model cached successfully!'); \
    "; \
    else \
    echo "HF_TOKEN not provided - model will be downloaded at runtime"; \
    fi

# Clean up unnecessary files
RUN find /opt/venv -name "*.pyc" -delete && \
    find /opt/venv -name "__pycache__" -type d -exec rm -rf {} + && \
    find /opt/venv -name "*.egg-info" -type d -exec rm -rf {} + && \
    pip cache purge

# --- Stage 2: Production ---
FROM python:3.12-slim

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN useradd --create-home --shell /bin/bash --uid 1000 app

WORKDIR /app

# Copy optimized virtual environment
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY --chown=app:app src/ ./src/
COPY --chown=app:app config/ ./config/

# Set optimized environment variables
ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TOKENIZERS_PARALLELISM=false \
    TRANSFORMERS_CACHE=/opt/venv/model_cache \
    HF_HOME=/opt/venv/model_cache \
    PYTORCH_DISABLE_WARNINGS=1

# Switch to non-root user
USER app

# Minimal health check
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=2 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)" || exit 1

EXPOSE 8000

# Optimized startup command for Railway free tier
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--access-log"]