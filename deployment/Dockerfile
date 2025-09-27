# Optimized multi-stage build for GitHub Actions with Git LFS support
FROM python:3.13-slim AS builder

# Install system dependencies
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

# Copy requirements
COPY requirements-prod.txt ./

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install PyTorch CPU versions first, explicitly providing the extra index URL
RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    torch==2.2.1+cpu \
    torchvision==0.17.1+cpu \
    torchaudio==2.2.1+cpu

# Install the rest of the dependencies
RUN pip install --no-cache-dir -r requirements-prod.txt

# Clean up pip cache
RUN pip cache purge

# --- Production stage ---
FROM python:3.13-slim

# Install runtime dependencies
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

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
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

# Expose port
EXPOSE 8000