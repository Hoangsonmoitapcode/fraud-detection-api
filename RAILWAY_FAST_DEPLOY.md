# 🚀 Railway Ultra-Fast Deployment Guide

## 🎯 Mục tiêu: Deploy trong 30 giây thay vì 10 phút

### ⚡ Cách hoạt động:
1. **GitHub Actions** build Docker image (chỉ khi code thay đổi)
2. **Railway** pull pre-built image (siêu nhanh!)

## 📋 Bước 1: Setup GitHub Actions (Một lần duy nhất)

### Trigger build lần đầu:
```powershell
./trigger-build.ps1 "Initial Docker image build"
```

### Hoặc manual trigger:
1. Vào GitHub Actions: https://github.com/hoangsonmoitapcode/fraud-detection-api/actions
2. Click "Build and Push Docker Image"
3. Click "Run workflow"

## 📋 Bước 2: Tạo Railway Service từ Docker Image

### Option A: Tạo service mới (RECOMMENDED)
1. **Xóa service cũ** đang build từ source
2. **Create New Service** → "Deploy from Docker Image"
3. **Image URL**: `ghcr.io/hoangsonmoitapcode/fraud-detection-api:latest`
4. **Environment Variables**:
   ```env
   DATABASE_URL=postgresql://...
   PORT=8000
   ENVIRONMENT=production
   ```

### Option B: Chuyển service hiện tại
1. Vào Railway project settings
2. Change source từ GitHub → Docker Image
3. Image: `ghcr.io/hoangsonmoitapcode/fraud-detection-api:latest`

## ⏱️ Timeline So Sánh:

| Method | Initial Setup | Each Deploy | Total Time |
|--------|---------------|-------------|------------|
| **Old (Source Build)** | 0min | 5-10min | **5-10min** 🐌 |
| **New (Pre-built)** | 5min | 30sec | **30sec** ⚡ |

## 🔄 Workflow Mới:

### Khi cần update code:
1. **Edit code** → commit → push
2. **GitHub Actions tự động build** (nếu có thay đổi quan trọng)
3. **Railway tự động redeploy** (30 giây)

### Khi chỉ update docs/config:
1. **Edit files** → commit → push  
2. **Không build image** (tiết kiệm thời gian)
3. **Railway không redeploy** (không cần thiết)

### Khi cần force rebuild:
```powershell
./trigger-build.ps1 "Add new features"
```

## 🎯 Files Trigger Build:
- `src/**` (source code)
- `requirements*.txt` (dependencies)
- `Dockerfile` (container config)
- `cache_models.py` (model setup)

## 🎯 Files KHÔNG Trigger Build:
- `*.md` (documentation)
- `*.ps1` (scripts)
- `railway.json` (config)
- Other config files

## 🔥 Benefits:

✅ **Ultra-fast deployments** (30 seconds)  
✅ **Intelligent builds** (only when needed)  
✅ **No build timeouts** on Railway free plan  
✅ **Consistent environments** across deployments  
✅ **Pre-cached models** and dependencies  
✅ **Version control** for Docker images  

## 🚨 Important Notes:

1. **First build takes 5-10 minutes** (one-time setup)
2. **Subsequent deploys take 30 seconds** 
3. **Build only triggers for important file changes**
4. **Manual trigger available** when needed
5. **Railway pulls image instead of building**

## 🔧 Troubleshooting:

### Image not found:
- Check GitHub Actions completed successfully
- Verify image exists: `ghcr.io/hoangsonmoitapcode/fraud-detection-api:latest`

### Railway still building from source:
- Check railway.json uses `"builder": "DOCKER"`
- Verify `dockerImage` URL is correct

### Need to force rebuild:
```powershell
./trigger-build.ps1 "Force rebuild"
```
