# --- Builder Stage: Local / Training / Testing ---
FROM python:3.12 AS builder

WORKDIR /app
COPY requirements.txt ./requirements.txt

# Cập nhật pip và cài full packages (có PyTorch + torchvision)
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

# --- Production Stage: Railway / Deployment ---
FROM python:3.12

WORKDIR /app

# Copy chỉ packages prod (không có PyTorch)
COPY requirements-prod.txt ./requirements-prod.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy source code
COPY src/ ./src/
COPY config/ ./config/

# Thiết lập biến môi trường
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MODEL_PATH=/app/phobert_sms_classifier.pkl \
    TOKENIZERS_PARALLELISM=false

EXPOSE 8000
