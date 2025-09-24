# 🚀 Railway Deployment Guide

## Quick Deployment Options

### Option 1: Pre-built Docker Image (⚡ FASTEST - 30 seconds)

1. **Use GitHub Actions** (Automatic):
   - Push to main branch → GitHub Actions automatically builds and pushes image
   - Image available at: `ghcr.io/hoangsonmoitapcode/fraud-detection-api:latest`

2. **Deploy on Railway**:
   - Create new service → "Deploy from Docker Image"
   - Use image: `ghcr.io/hoangsonmoitapcode/fraud-detection-api:latest`
   - Add environment variables (DATABASE_URL, etc.)

### Option 2: Manual Docker Build

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Build and push (Windows)
./build-and-push.ps1

# Build and push (Linux/Mac)
./build-and-push.sh
```

### Option 3: Railway Build from Source (⏳ SLOWER - 5-10 minutes)

- Use `railway.json` configuration
- Railway builds from Dockerfile

## Performance Comparison

| Method | Build Time | Deploy Time | Total Time |
|--------|------------|-------------|------------|
| Pre-built Image | 0s | 30s | **30s** ⚡ |
| Railway Build | 5-10min | 30s | **5-10min** |

## Environment Variables

Required for all deployment methods:

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
PORT=8000
ENVIRONMENT=production
```

## Troubleshooting

### Build Timeout Issues
- Use pre-built image option
- Upgrade to Railway Pro ($5/month)
- Reduce dependencies in requirements.txt

### Image Size Optimization
- Current image: ~3GB (includes all ML models)
- For lighter deployment: Use CPU-only PyTorch
- For production: Pre-cache models in image

## Architecture

```
GitHub → GitHub Actions → GHCR → Railway
   ↓           ↓            ↓        ↓
 Code     Build Image   Store    Deploy
```

## Benefits of Pre-built Images

✅ **Ultra-fast deployment** (30 seconds vs 10 minutes)  
✅ **Consistent builds** across environments  
✅ **Pre-cached dependencies** and models  
✅ **No build timeouts** on Railway free plan  
✅ **Automatic builds** via GitHub Actions  
✅ **Version control** for deployments
