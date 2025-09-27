# --- Builder Stage: Local / Training / Testing ---
FROM python:3.12 AS builder

WORKDIR /app
COPY requirements.txt ./requirements.txt

# Upgrade pip, setuptools, wheel để tránh lỗi metadata
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Cài tất cả dependencies local (có PyTorch)
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

# --- Production Stage: Railway / Deployment ---
FROM python:3.12

WORKDIR /app

# Copy chỉ packages prod (không có PyTorch)
COPY requirements-prod.txt ./requirements-prod.txt
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy source code
COPY src/ ./src/
COPY config/ ./config/

ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MODEL_PATH=/app/phobert_sms_classifier.pkl \
    TOKENIZERS_PARALLELISM=false

EXPOSE 8000
