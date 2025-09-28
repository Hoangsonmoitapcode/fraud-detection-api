# --- Giai đoạn 1: Builder (multi-stage để giảm size) ---
FROM python:3.12-slim AS builder

# Cài các công cụ cần thiết để build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Sao chép file requirements
COPY requirements.txt ./

# Nâng cấp pip
RUN pip install --no-cache-dir --upgrade pip

# Cài các package trực tiếp (CPU-only PyTorch)
RUN pip install --no-cache-dir \
    torch>=2.5.0+cpu \
    torchvision>=0.20.0+cpu \
    torchaudio>=2.6.0+cpu \
    && pip install --no-cache-dir -r requirements.txt

# --- Giai đoạn 2: Production ---
FROM python:3.12-slim

# Cài các gói hệ điều hành tối thiểu để chạy app
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Tạo user không phải root
RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

# chép site-packages từ builder sang (không cần venv)
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Sao chép code ứng dụng
COPY src/ ./src/
COPY config/ ./config/

# Biến môi trường cần thiết
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TOKENIZERS_PARALLELISM=false

# Chuyển quyền và dùng user mới
RUN chown -R app:app /app
USER app

EXPOSE 8000
