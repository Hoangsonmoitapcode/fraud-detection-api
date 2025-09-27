# Optimized multi-stage build for GitHub Actions with Git LFS support
FROM python:3.11-slim as builder

# Install system dependencies including Git LFS
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    git-lfs \
    curl \
    wget \
    && git lfs install \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies with error handling
COPY requirements-prod.txt ./
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements-prod.txt && \
    pip cache purge

# Production stage - minimal base
FROM python:3.11-slim

# Install runtime dependencies including Git LFS for model files
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    git \
    git-lfs \
    ca-certificates \
    && git lfs install \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /app

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Copy only essential Python packages
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code first
COPY src/ ./src/
COPY config/ ./config/

# Handle Git LFS model file with verification
COPY .git ./.git
COPY .gitattributes ./
COPY phobert_sms_classifier.pkl ./

# Verify model file integrity and fallback mechanism
RUN ls -la phobert_sms_classifier.pkl && \
    echo "Model file size: $(du -h phobert_sms_classifier.pkl)" && \
    if [ ! -f phobert_sms_classifier.pkl ] || [ $(stat -f%z phobert_sms_classifier.pkl 2>/dev/null || stat -c%s phobert_sms_classifier.pkl) -lt 100000000 ]; then \
    echo "WARNING: Model file missing or too small - will attempt Git LFS pull"; \
    git lfs pull 2>/dev/null || echo "Git LFS pull failed - model will load from fallback"; \
    fi

# Set environment variables for better performance
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MODEL_PATH=/app/phobert_sms_classifier.pkl \
    TOKENIZERS_PARALLELISM=false

# Change ownership to app user
RUN chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Comprehensive health check with model verification
HEALTHCHECK --interval=60s --timeout=30s --start-period=120s --retries=5 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application with proper startup sequence
CMD ["sh", "-c", "echo 'Starting Fraud Detection API...' && python -c 'from src.sms_prediction_service import sms_prediction_service; print(f\"Model loading test: {sms_prediction_service.load_model()}\")' && python -m uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1 --timeout-keep-alive 30"]