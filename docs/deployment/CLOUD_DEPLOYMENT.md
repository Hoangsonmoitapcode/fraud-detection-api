# ☁️ Cloud Deployment Guide

## 🎯 **Mục Tiêu**
Deploy API lên cloud để người khác có thể gọi qua internet:
- `https://your-api-domain.com/analyze/`
- `https://your-api-domain.com/health`
- Database chạy cùng server hoặc riêng biệt

## 🏗️ **Architecture**

```
Internet Users
      │
      ▼
┌─────────────────────┐
│   Cloud Platform    │
│                     │
│  ┌───────────────┐  │
│  │   FastAPI     │  │  ← Your API Code
│  │   Server      │  │
│  └───────────────┘  │
│           │         │
│  ┌───────────────┐  │
│  │  PostgreSQL   │  │  ← Your Database
│  │   Database    │  │
│  └───────────────┘  │
└─────────────────────┘
```

## 🌐 **Cloud Platform Options**

### **1. 🔥 Railway (Dễ nhất - Free tier)**

#### **Ưu điểm:**
- ✅ Free tier với PostgreSQL
- ✅ Auto-deploy từ GitHub
- ✅ HTTPS tự động
- ✅ Environment variables
- ✅ Logs và monitoring

#### **Setup Steps:**
```bash
# 1. Cài Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Tạo project
railway new

# 4. Deploy
railway up
```

#### **Config Files cần tạo:**
```yaml
# railway.json
{
  "deploy": {
    "startCommand": "python -m uvicorn src.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health"
  }
}
```

### **2. 🐳 Render (Free tier)**

#### **Ưu điểm:**
- ✅ Free tier
- ✅ PostgreSQL free
- ✅ GitHub integration
- ✅ Auto SSL
- ✅ Easy setup

#### **Setup Steps:**
1. Push code lên GitHub
2. Connect GitHub repo tới Render
3. Set environment variables
4. Deploy

### **3. 🌊 Heroku (Paid)**

#### **Setup Steps:**
```bash
# 1. Install Heroku CLI
# 2. Login
heroku login

# 3. Create app
heroku create your-fraud-api

# 4. Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# 5. Deploy
git push heroku main
```

### **4. ☁️ AWS/GCP/Azure (Advanced)**

## 📝 **Chuẩn Bị Code cho Deployment**

### **1. Tạo Procfile (cho Heroku)**
```bash
# Procfile
web: python -m uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

### **2. Cập nhật requirements.txt**
```bash
# Thêm vào config/requirements.txt
gunicorn==21.2.0
python-dotenv==1.0.0
```

### **3. Tạo runtime.txt**
```bash
# runtime.txt
python-3.11.7
```

### **4. Cập nhật database.py cho production**
```python
# src/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Production database URL từ environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Fix cho Heroku PostgreSQL URL
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Fallback cho local development
if not DATABASE_URL:
    DATABASE_URL = "postgresql+psycopg2://fastapi_user:mypassword@localhost:5432/fastapi_db"

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

### **5. Cập nhật main.py cho production**
```python
# src/main.py - Thêm CORS cho web clients
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Fraud Detection API",
    description="Comprehensive fraud detection API",
    version="3.1.1"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production, chỉ định domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🔧 **Environment Variables cần set**

```bash
# Trên cloud platform
DATABASE_URL=postgresql://user:pass@host:port/db
PORT=8000
PYTHONPATH=/app/src
```

## 📋 **Deployment Checklist**

### **Pre-deployment:**
- [ ] ✅ Code tested locally
- [ ] ✅ Database populated with phone headings
- [ ] ✅ Environment variables configured
- [ ] ✅ Requirements.txt updated
- [ ] ✅ CORS configured
- [ ] ✅ Health check endpoint working

### **Post-deployment:**
- [ ] ✅ API accessible via HTTPS
- [ ] ✅ Health check returns 200
- [ ] ✅ Database connection working
- [ ] ✅ Phone analysis working
- [ ] ✅ All endpoints responding
- [ ] ✅ Logs monitoring setup

## 🧪 **Testing Deployed API**

### **Test Commands:**
```bash
# Replace YOUR_API_URL with actual deployed URL
export API_URL="https://your-fraud-api.railway.app"

# Test health
curl $API_URL/health

# Test phone analysis
curl -X POST "$API_URL/analyze/" \
  -H "Content-Type: application/json" \
  -d '{"phone_numbers": ["0965842855", "0870123456"]}'

# Test new carriers
curl -X POST "$API_URL/analyze/" \
  -H "Content-Type: application/json" \
  -d '{"phone_numbers": ["0920123456", "0990123456", "0890123456"]}'
```

## 🔒 **Security cho Production**

### **1. API Rate Limiting**
```python
# pip install slowapi
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/analyze/")
@limiter.limit("100/minute")  # Limit 100 requests per minute
def analyze_phone_numbers(request: Request, ...):
    # Your code
```

### **2. API Authentication (Optional)**
```python
# Thêm API key authentication
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header()):
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@app.post("/analyze/", dependencies=[Depends(verify_api_key)])
def analyze_phone_numbers(...):
    # Your code
```

### **3. HTTPS Only**
```python
# Redirect HTTP to HTTPS
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
app.add_middleware(HTTPSRedirectMiddleware)
```

## 📊 **Monitoring & Analytics**

### **1. Logging**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/analyze/")
def analyze_phone_numbers(...):
    logger.info(f"Analyzing {len(phone_numbers)} phone numbers")
    # Your code
```

### **2. Usage Analytics**
```python
# Track API usage
@app.post("/analyze/")
def analyze_phone_numbers(...):
    # Log usage to database or external service
    # Track: timestamp, endpoint, user_ip, response_time
```

## 💰 **Cost Estimation**

### **Free Tiers:**
- **Railway**: Free với limits
- **Render**: Free với sleep mode
- **Heroku**: $7/month cho hobby tier

### **Paid Options:**
- **Railway Pro**: $5/month
- **Render Pro**: $7/month  
- **Heroku Standard**: $25/month
- **AWS/GCP**: $10-50/month tùy usage

## 🎯 **Recommended Approach**

### **Phase 1: Start with Railway (Free)**
1. Deploy lên Railway free tier
2. Test với vài users
3. Monitor performance và usage

### **Phase 2: Scale if needed**
1. Upgrade Railway plan
2. Hoặc migrate sang AWS/GCP
3. Add CDN và load balancing

## 📞 **User Integration Examples**

Sau khi deploy, users có thể gọi API như này:

### **JavaScript/Web:**
```javascript
// Analyze phone numbers
const response = await fetch('https://your-api.railway.app/analyze/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        phone_numbers: ['0965842855', '0870123456']
    })
});
const data = await response.json();
console.log(data);
```

### **Python:**
```python
import requests

response = requests.post('https://your-api.railway.app/analyze/', 
                        json={'phone_numbers': ['0965842855']})
print(response.json())
```

### **cURL:**
```bash
curl -X POST "https://your-api.railway.app/analyze/" \
  -H "Content-Type: application/json" \
  -d '{"phone_numbers": ["0965842855"]}'
```

---

## 🎉 **Next Steps**

1. **Choose platform**: Railway (easiest) hoặc Render
2. **Prepare code**: Add Procfile, update database.py
3. **Deploy**: Push to GitHub → Connect to platform
4. **Test**: Verify all endpoints work
5. **Share**: Give users your API URL
6. **Monitor**: Track usage và performance

**🚀 Sau khi deploy, bạn sẽ có API public mà ai cũng có thể gọi qua internet!**
