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

# Upgrade pip and install build tools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install PyTorch CPU versions with specific index URL (using stable versions)
RUN pip install --no-cache-dir \
    --index-url https://download.pytorch.org/whl/cpu \
    torch==2.0.1+cpu \
    torchvision==0.15.2+cpu \
    torchaudio==2.0.2+cpu

# Install remaining dependencies
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

# Setup Git LFS and pull model file
COPY .git ./.git
COPY .gitattributes ./

# Force Git LFS pull to get actual model file
RUN git lfs install && \
    git lfs pull && \
    ls -la phobert_sms_classifier.pkl && \
    echo "Model file size after LFS pull: $(du -h phobert_sms_classifier.pkl)"

# Verify model file integrity  
RUN if [ ! -f phobert_sms_classifier.pkl ] || [ $(stat -f%z phobert_sms_classifier.pkl 2>/dev/null || stat -c%s phobert_sms_classifier.pkl) -lt 100000000 ]; then \
    echo "❌ Model file still too small after Git LFS pull"; \
    echo "File size: $(stat -c%s phobert_sms_classifier.pkl 2>/dev/null || echo 'File not found')"; \
    exit 1; \
    else \
    echo "✅ Model file loaded successfully: $(du -h phobert_sms_classifier.pkl)"; \
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

# No health check - handled by Railway configuration
# No CMD - Railway will use startCommand from railway.json