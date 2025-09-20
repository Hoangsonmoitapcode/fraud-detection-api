# 🚀 Deployment Guide

## 📋 **Quick Deploy to Railway**

### **Step 1: Railway Setup**
1. Go to https://railway.app
2. Login with GitHub
3. New Project → Deploy from GitHub repo
4. Select: `Hoangsonmoitapcode/fraud-detection-api`
5. Add PostgreSQL database

### **Step 2: Get API URL**
- Railway dashboard → Settings → Domains
- Copy URL: `https://fraud-detection-api-production-xxxx.up.railway.app`

### **Step 3: Test API**
```bash
curl https://your-url/health
curl https://your-url/docs
```

## 👥 **For Users**

Users only need:
- ✅ Your API URL
- ✅ Internet connection
- ✅ HTTP client (curl, JavaScript, Python requests, etc.)

**No installation required for users!**

### **Example Usage:**
```javascript
const response = await fetch('https://your-api-url/analyze/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        phone_numbers: ['0965842855', '0870123456']
    })
});
const data = await response.json();
```

## 📱 **Supported Features**
- Phone fraud detection (Vietnamese + International)
- SMS spam detection
- Banking scam verification
- Website safety checking
- Batch processing for all endpoints
