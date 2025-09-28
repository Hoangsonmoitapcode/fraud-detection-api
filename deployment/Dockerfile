# --- Giai đoạn 1: Builder (Xưởng chế tạo) ---
FROM python:3.12-slim AS builder

# Cài công cụ build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Sao chép file requirements (có torch CPU)
COPY requirements.txt ./

# Nâng cấp pip
RUN pip install --no-cache-dir --upgrade pip

# Tạo môi trường ảo
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# ⚡ Cài đặt tất cả gói (ép chỉ dùng CPU build)
RUN pip install --no-cache-dir -r requirements.txt \
    --extra-index-url https://download.pytorch.org/whl/cpu


# --- Giai đoạn 2: Production (Image cuối cùng) ---
FROM python:3.12-slim

# Cài gói hệ điều hành tối thiểu
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Tạo user không phải root
RUN useradd --create-home --shell /bin/bash app
WORKDIR /app

# Copy môi trường ảo từ builder
COPY --from=builder /opt/venv /opt/venv

# Copy code
COPY src/ ./src/
COPY config/ ./config/

# Kích hoạt môi trường ảo và env khác
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TOKENIZERS_PARALLELISM=false

# Quyền user
RUN chown -R app:app /app
USER app

EXPOSE 8000
