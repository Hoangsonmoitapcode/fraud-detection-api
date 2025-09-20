# 📱 Fraud Detection API - For Users

## 🎯 **What This API Does**
Detect fraud for Vietnamese phone numbers, SMS content, banking accounts, and websites.

## 🌐 **API Information**
- **Base URL**: `https://your-api-url.up.railway.app` *(will be updated after deployment)*
- **Documentation**: `https://your-api-url.up.railway.app/docs`
- **Health Check**: `https://your-api-url.up.railway.app/health`

## ⚡ **Quick Examples**

### **Analyze Phone Numbers**
```bash
curl -X POST "https://your-api-url.up.railway.app/analyze/" \
  -H "Content-Type: application/json" \
  -d '{"phone_numbers": ["0965842855", "0870123456", "0920123456"]}'
```

**Response:**
```json
{
  "summary": {
    "total_analyzed": 3,
    "high_risk_count": 0,
    "low_risk_count": 3,
    "processing_time": 0.15
  },
  "results": [
    {
      "phone_number": "0965842855",
      "analysis": {
        "phone_head": "096",
        "phone_region": "Vietnam",
        "label": "safe"
      },
      "fraud_risk": "LOW"
    }
  ]
}
```

## 💻 **Programming Examples**

### **JavaScript**
```javascript
async function checkPhones(numbers) {
    const response = await fetch('https://your-api-url.up.railway.app/analyze/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone_numbers: numbers })
    });
    return await response.json();
}

// Usage
const result = await checkPhones(['0965842855', '0870123456']);
console.log(result);
```

### **Python**
```python
import requests

def check_phones(numbers):
    response = requests.post(
        'https://your-api-url.up.railway.app/analyze/',
        json={'phone_numbers': numbers}
    )
    return response.json()

# Usage
result = check_phones(['0965842855', '0870123456'])
print(result)
```

## 📱 **Supported Vietnamese Carriers**

| Carrier | Prefixes | Status |
|---------|----------|--------|
| **Traditional** | 096, 097, 098, 032-039, 070, 076-079, 081-085, 088, 091, 094 | ✅ SAFE |
| **iTel** | 087 | ✅ SAFE |
| **Vietnamobile** | 092, 056, 058 | ✅ SAFE |
| **Wintel** | 099 | ✅ SAFE |
| **VNPAY Sky** | 089 | ✅ SAFE |

## 🔧 **No Installation Required!**

You DON'T need to install:
- ❌ Python
- ❌ PostgreSQL  
- ❌ Any special software

You ONLY need:
- ✅ Internet connection
- ✅ Your preferred programming language
- ✅ The API URL (provided after deployment)

## 📚 **Full Documentation**

Visit the interactive documentation at:
`https://your-api-url.up.railway.app/docs`

You can test all endpoints directly in your browser!

---

**🎉 Easy to use, no setup required!**
