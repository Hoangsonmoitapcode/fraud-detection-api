# 🧪 Local Testing Guide - Fraud Detection API

## Prerequisites ✅

1. **Python 3.12** installed
2. **HF_TOKEN** environment variable set
3. **Git** repository cloned locally

## Quick Local Setup 🚀

### Step 1: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
# Install CPU-only PyTorch (to match production)
pip install torch>=2.8.0+cpu torchvision>=0.23.0+cpu torchaudio>=2.8.0+cpu \
  --index-url https://download.pytorch.org/whl/cpu

# Install other dependencies
pip install -r requirements.txt

# OR install from production requirements
pip install -r requirements_prod.txt
```

### Step 3: Set Environment Variables
```bash
# Windows PowerShell
$env:HF_TOKEN = "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"

# Windows Command Prompt
set HF_TOKEN=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

# Linux/Mac
export HF_TOKEN=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
```

### Step 4: Run Locally
```bash
# Run the FastAPI server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Testing Your API 🧪

### Test 1: Basic Health Check
```bash
curl http://localhost:8000/ping
```
**Expected Result**: `{"status": "ok", "message": "pong"}`

### Test 2: API Root Endpoint
```bash
curl http://localhost:8000/
```
**Expected Result**: API information with features listed

### Test 3: Model Status (Before Loading)
```bash
curl http://localhost:8000/model-status
```
**Expected Result**: Model info with `is_loaded: false`

### Test 4: Load Model ⚠️ BIG TEST
```bash
curl -X POST http://localhost:8000/load-model
```
**Expected Result**: 
- Takes 3-5 minutes (downloading 518MB model)
- Returns success with model info

### Test 5: SMS Prediction
```bash
curl -X POST http://localhost:8000/predict-sms/ \
  -H "Content-Type: application/json" \
  -d '{"sms_content": "Tin nhắn spam test"}'
```

### Test 6: Phone Analysis
```bash
curl -X POST http://localhost:8000/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"phone_numbers": ["0123456789"]}'
```

## Common Issues & Solutions 🔧

### Issue 1: HF_TOKEN not recognized
```bash
# Check if environment variable is set
echo $HF_TOKEN  # Linux/Mac
echo %HF_TOKEN% # Windows CMD
echo $env:HF_TOKEN # Windows PowerShell
```

### Issue 2: Torch installation fails
```bash
# Clear pip cache and reinstall
pip cache purge
pip install -r requirements_prod.txt --no-cache-dir
```

### Issue 3: Module import errors
```bash
# Check Python path
export PYTHONPATH=/path/to/your/project
# OR run from project root
cd /path/to/fraud-detection-api
uvicorn src.main:app --reload
```

### Issue 4: Database connection errors
The API will work for SMS prediction even without database connection.

## Docker Testing 🐳

### Build Docker Image Locally
```bash
# Build image
docker build -f deployment/Dockerfile -t fraud-detection-api .

# Run container
docker run -p 8000:8000 \
  -e HF_TOKEN=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 \
  fraud-detection-api
```

### Check Image Size
```bash
docker images fraud-detection-api
```
**Expected**: < 3GB (optimized for Railway free tier)

## Testing Checklist ✅

Before pushing to GitHub:

- [ ] ✅ Local API starts successfully (`uvicorn` runs)
- [ ] ✅ Health check works (`/ping` returns 200)
- [ ] ✅ HF_TOKEN is properly loaded
- [ ] ✅ Model loads without errors (`/load-model`)
- [ ] ✅ SMS prediction works (`/predict-sms/`)
- [ ] ✅ Docker image builds successfully
- [ ] ✅ Docker image size < 3GB
- [ ] ✅ No Python linting errors

## Performance Expectations 📊

### Local Environment
- **Model Load Time**: 3-5 minutes (first time)
- **Prediction Time**: < 1 second (after model loaded)
- **Memory Usage**: ~1.5GB (with model loaded)

### Railway Production
- **First Deploy**: 10-15 minutes (building + deploying)
- **Model Load**: 5-8 minutes (518MB download)
- **Cold Start**: ~30 seconds

## Push to GitHub 🚀

Once local testing passes:

```bash
# Add all changes
git add .

# Commit with descriptive message
git commit -m "Fix pickle loading and optimize for Railway free tier

- Added CompletePhoBERTClassifier class definition
- Optimized Dockerfile for CPU-only PyTorch
- Enhanced Railway configuration
- Added comprehensive error handling
- Fixed HuggingFace repository metadata"

# Push to trigger deployment
git push origin main
```

## Monitor Deployment 📈

1. **GitHub Actions**: Check build progress
2. **Railway Dashboard**: Monitor deployment logs
3. **Model Loading**: Test `/load-model` endpoint once deployed

---

**🎯 Success Criteria**: 
- API responds to health checks
- Model loads successfully
- SMS predictions work accurately
- Docker image < 3GB
- Railway deployment successful

Good luck with your deployment! 🚀
