# Heavy pre-built Docker image with ALL dependencies
FROM python:3.11-slim

# Install ALL system dependencies (both build and runtime)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    libpq5 \
    git \
    curl \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install ALL dependencies
COPY requirements.txt requirements-prod.txt ./
RUN pip install --no-cache-dir --upgrade pip

# Install FULL dependencies (including CUDA if needed)
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download common ML models to cache them
RUN python -c "
import torch
import transformers
from transformers import AutoTokenizer, AutoModel
print('Pre-caching models...')
try:
# Cache common Vietnamese models
tokenizer = AutoTokenizer.from_pretrained('vinai/phobert-base')
model = AutoModel.from_pretrained('vinai/phobert-base')
print('PhoBERT cached successfully')
except:
print('PhoBERT cache failed, will download at runtime')
"

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app

# Pre-compile Python bytecode
RUN python -m compileall src/

USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
