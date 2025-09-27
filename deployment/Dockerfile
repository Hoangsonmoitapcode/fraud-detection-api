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

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install PyTorch CPU versions first, explicitly providing the index URL
RUN pip install --no-cache-dir \
    --index-url https://download.pytorch.org/whl/cpu \
    torch==2.0.1+cpu \
    torchvision==0.15.2+cpu \
    torchaudio==2.0.2+cpu

# Install the rest of the dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements-prod.txt

# Clean up pip cache
RUN pip cache purge

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

# Model will be downloaded from HuggingFace Hub at runtime
# No need to copy model file - it will be downloaded when needed

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

# No health check - handled by Railway configuration
# No CMD - Railway will use startCommand from railway.json