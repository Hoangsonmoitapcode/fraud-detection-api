# Railway Deployment Guide

## 🚀 Tạo Railway Service

### Bước 1: Tạo Project
1. Đăng nhập: https://railway.app
2. Click "New Project"
3. Chọn "Empty Project"

### Bước 2: Thêm Service
1. Click "New Service"
2. Chọn "GitHub Repo"
3. Chọn repository: `Hoangsonmoitapcode/fraud-detection-api`

### Bước 3: Cấu hình Environment Variables

Vào **Settings** → **Variables** và thêm các biến sau:

#### Required Variables:
```bash
# Database
DATABASE_URL=postgresql://postgres:password@postgres.railway.internal:5432/railway

# Application
PORT=8000
ENVIRONMENT=production

# Optional Variables:
# LOG_LEVEL=INFO
# WORKERS=1
```

### Bước 4: Cấu hình Deploy Settings

Vào **Settings** → **Deploy**:
- **Build Command**: (để trống)
- **Start Command**: (để trống)
- **Dockerfile Path**: `Dockerfile`

### Bước 5: Thêm PostgreSQL Database

1. Click "New Service"
2. Chọn "Database" → "PostgreSQL"
3. Railway sẽ tự động tạo `DATABASE_URL`

## 🔧 Cấu hình Chi tiết

### Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `DATABASE_URL` | `postgresql://...` | PostgreSQL connection string (auto-generated) |
| `PORT` | `8000` | Application port (Railway sets automatically) |
| `ENVIRONMENT` | `production` | Environment mode |
| `LOG_LEVEL` | `INFO` | Logging level (optional) |
| `WORKERS` | `1` | Number of workers (optional) |

### Service URLs

Sau khi deploy thành công:
- **API URL**: `https://your-service-name.up.railway.app`
- **Health Check**: `https://your-service-name.up.railway.app/health`
- **API Docs**: `https://your-service-name.up.railway.app/docs`

## 🧪 Test API

### Health Check
```bash
curl https://your-service-name.up.railway.app/health
```

### SMS Prediction
```bash
curl -X POST "https://your-service-name.up.railway.app/predict/sms" \
     -H "Content-Type: application/json" \
     -d '{"message": "Chào bạn, đây là tin nhắn test"}'
```

## 🔍 Troubleshooting

### Kiểm tra Logs
1. Vào **Deployments** tab
2. Click vào deployment mới nhất
3. Xem logs để debug

### Common Issues
1. **Database connection failed**: Kiểm tra `DATABASE_URL`
2. **Model not loaded**: Kiểm tra logs xem model có load được không
3. **Port issues**: Railway tự động set PORT, không cần config

## 📊 Monitoring

- **Metrics**: Vào **Metrics** tab để xem CPU, Memory usage
- **Logs**: Real-time logs trong **Deployments** tab
- **Health**: API endpoint `/health` để check status
