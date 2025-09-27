# --- Build Stage ---
FROM python:3.12 AS builder

# Cài đặt các phụ thuộc hệ thống
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev git git-lfs curl wget \
    && git lfs install && rm -rf /var/lib/apt/lists/* && apt-get clean

WORKDIR /app
COPY requirements-prod.txt ./requirements-prod.txt

# Cập nhật pip
RUN pip install --no-cache-dir --upgrade pip

# Cài đặt các thư viện
RUN pip install --no-cache-dir -r requirements-prod.txt

# --- Production Stage ---
FROM python:3.12

# Cài đặt các phụ thuộc cần thiết
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 curl git git-lfs ca-certificates \
    && git lfs install && rm -rf /var/lib/apt/lists/* && apt-get clean

RUN useradd --create-home --shell /bin/bash app
WORKDIR /app

# Sao chép các gói Python từ builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Sao chép mã nguồn ứng dụng
COPY src/ ./src/
COPY config/ ./config/

# Thiết lập các biến môi trường
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MODEL_PATH=/app/phobert_sms_classifier.pkl \
    TOKENIZERS_PARALLELISM=false

# Thay đổi quyền sở hữu và chuyển sang người dùng không phải root
RUN chown -R app:app /app
USER app

EXPOSE 8000
