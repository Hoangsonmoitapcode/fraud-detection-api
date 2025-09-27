# --- Giai đoạn 1: Builder (Xưởng chế tạo) ---
# Sử dụng Python 3.12-slim để build, giúp giảm dung lượng cache và build nhanh hơn
FROM python:3.12-slim AS builder

# Cài các công cụ cần thiết để build thư viện
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Sao chép các file requirements
COPY requirements.txt ./
COPY requirements-prod.txt ./

# Nâng cấp pip
RUN pip install --no-cache-dir --upgrade pip

# Cài đặt TẤT CẢ các thư viện vào một môi trường ảo tạm thời
# Bước này sẽ sử dụng file requirements.txt (có PyTorch) để cài đặt
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt


# --- Giai đoạn 2: Production (Image cuối cùng, gọn nhẹ) ---
# Bắt đầu từ một image slim sạch sẽ
FROM python:3.12-slim

# Cài các gói hệ điều hành tối thiểu cần thiết để CHẠY ứng dụng
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Tạo user không phải root để tăng bảo mật
RUN useradd --create-home --shell /bin/bash app
WORKDIR /app

# *** Bước quan trọng nhất: Sao chép các gói đã cài từ builder ***
# Chỉ sao chép các thư viện đã được cài, không cần cài lại từ đầu
COPY --from=builder /opt/venv /opt/venv

# Sao chép code ứng dụng
COPY src/ ./src/
COPY config/ ./config/

# Kích hoạt môi trường ảo và đặt các biến môi trường khác
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TOKENIZERS_PARALLELISM=false

# Chuyển quyền và sử dụng user mới
RUN chown -R app:app /app
USER app

EXPOSE 8000