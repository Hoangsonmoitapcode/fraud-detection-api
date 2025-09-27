# --- Build Stage ---
FROM python:3.12 AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev git git-lfs curl wget \
    && git lfs install && rm -rf /var/lib/apt/lists/* && apt-get clean

WORKDIR /app
COPY requirements-prod.txt ./requirements-prod.txt

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements-prod.txt

# --- Production Stage ---
FROM python:3.12

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 curl git git-lfs ca-certificates \
    && git lfs install && rm -rf /var/lib/apt/lists/* && apt-get clean

RUN useradd --create-home --shell /bin/bash app
WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MODEL_PATH=/app/phobert_sms_classifier.pkl \
    TOKENIZERS_PARALLELISM=false

# Change ownership and switch to non-root user
RUN chown -R app:app /app
USER app

EXPOSE 8000
