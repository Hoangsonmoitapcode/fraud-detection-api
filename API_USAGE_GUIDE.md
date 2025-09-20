# 📱 Fraud Detection API - Usage Guide

**Base URL:** `https://your-fraud-api.railway.app` (thay bằng URL thực của bạn)

## 🎯 **API Overview**

API này giúp phát hiện gian lận cho:
- 📱 **Phone Numbers**: Phân tích số điện thoại Việt Nam và quốc tế
- 💬 **SMS Content**: Phát hiện tin nhắn spam/lừa đảo
- 🏦 **Banking Accounts**: Kiểm tra tài khoản ngân hàng lừa đảo
- 🌐 **Websites**: Phát hiện website phishing/lừa đảo

## 🔧 **Quick Start**

### **1. Check API Status**
```bash
curl https://your-fraud-api.railway.app/
```

### **2. Health Check**
```bash
curl https://your-fraud-api.railway.app/health
```

### **3. View Interactive Documentation**
Mở browser: `https://your-fraud-api.railway.app/docs`

## 📱 **Phone Number Analysis**

### **Analyze Single Phone Number**
```bash
curl -X POST "https://your-fraud-api.railway.app/analyze/" \
  -H "Content-Type: application/json" \
  -d '{"phone_numbers": ["0965842855"]}'
```

**Response:**
```json
{
  "phone_number": "0965842855",
  "analysis": {
    "phone_head": "096",
    "phone_region": "Vietnam",
    "label": "safe",
    "heading_id": 1
  },
  "fraud_risk": "LOW"
}
```

### **Analyze Multiple Phone Numbers**
```bash
curl -X POST "https://your-fraud-api.railway.app/analyze/" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_numbers": [
      "0965842855",
      "0870123456", 
      "0920123456",
      "+1234567890"
    ]
  }'
```

**Response:**
```json
{
  "summary": {
    "total_analyzed": 4,
    "high_risk_count": 1,
    "low_risk_count": 3,
    "error_count": 0,
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
      "fraud_risk": "LOW",
      "status": "success"
    },
    {
      "phone_number": "+1234567890",
      "analysis": {
        "phone_head": "+1",
        "phone_region": "USA/Canada", 
        "label": "unsafe"
      },
      "fraud_risk": "HIGH",
      "status": "success"
    }
  ]
}
```

### **Supported Vietnamese Carriers**
| Carrier | Prefixes | Status |
|---------|----------|---------|
| **Traditional** | 096, 097, 098, 032-039, 070, 076-079, 081-085, 088, 091, 094 | ✅ SAFE |
| **iTel** | 087 | ✅ SAFE |
| **Vietnamobile** | 092, 056, 058 | ✅ SAFE |
| **Wintel** | 099 | ✅ SAFE |
| **VNPAY Sky** | 089 | ✅ SAFE |
| **Additional** | 059, 090, 093, 095 | ✅ SAFE |

## 💬 **SMS Scam Detection**

### **Report SMS Spam**
```bash
curl -X POST "https://your-fraud-api.railway.app/sms-scam/" \
  -H "Content-Type: application/json" \
  -d '{
    "sms_messages": [
      {
        "sms_content": "Chúc mừng! Bạn đã trúng thưởng 100 triệu đồng. Nhấn link để nhận ngay!",
        "label": "spam"
      },
      {
        "sms_content": "Tài khoản của bạn bị khóa. Vui lòng truy cập link để kích hoạt lại.",
        "label": "scam"
      }
    ]
  }'
```

### **Check SMS Content**
```bash
curl "https://your-fraud-api.railway.app/check-sms/?sms_content=Chúc%20mừng%20bạn%20trúng%20thưởng"
```

**Response:**
```json
{
  "sms_content": "Chúc mừng bạn trúng thưởng",
  "is_spam": true,
  "label": "spam",
  "risk_level": "HIGH",
  "match_type": "fuzzy",
  "similar_count": 3
}
```

## 🏦 **Banking Scam Detection**

### **Report Scam Banking Account**
```bash
curl -X POST "https://your-fraud-api.railway.app/banking-scam/" \
  -H "Content-Type: application/json" \
  -d '{
    "banking_accounts": [
      {
        "account_number": "1234567890",
        "bank_name": "Vietcombank"
      },
      {
        "account_number": "9876543210", 
        "bank_name": "Techcombank"
      }
    ]
  }'
```

### **Check Banking Account**
```bash
curl "https://your-fraud-api.railway.app/check-banking/?account_number=1234567890&bank_name=Vietcombank"
```

**Response:**
```json
{
  "account_number": "1234567890",
  "bank_name": "Vietcombank", 
  "is_scam": true,
  "risk_level": "HIGH"
}
```

## 🌐 **Website Scam Detection**

### **Report Scam Website**
```bash
curl -X POST "https://your-fraud-api.railway.app/website-scam/" \
  -H "Content-Type: application/json" \
  -d '{
    "websites": [
      {
        "website_url": "https://fake-bank-site.com",
        "label": "scam"
      },
      {
        "website_url": "https://phishing-site.net",
        "label": "phishing"
      }
    ]
  }'
```

### **Check Website Safety**
```bash
curl "https://your-fraud-api.railway.app/check-website/?website_url=https://suspicious-site.com"
```

**Response:**
```json
{
  "website_url": "https://suspicious-site.com",
  "is_scam": false,
  "label": "unknown",
  "risk_level": "LOW"
}
```

## 💻 **Programming Examples**

### **JavaScript/Node.js**
```javascript
// Analyze phone numbers
async function analyzePhones(numbers) {
    const response = await fetch('https://your-fraud-api.railway.app/analyze/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone_numbers: numbers })
    });
    return await response.json();
}

// Usage
const result = await analyzePhones(['0965842855', '0870123456']);
console.log(result);
```

### **Python**
```python
import requests

def analyze_phones(numbers):
    response = requests.post(
        'https://your-fraud-api.railway.app/analyze/',
        json={'phone_numbers': numbers}
    )
    return response.json()

# Usage
result = analyze_phones(['0965842855', '0870123456'])
print(result)
```

### **PHP**
```php
<?php
function analyzePhones($numbers) {
    $data = json_encode(['phone_numbers' => $numbers]);
    
    $ch = curl_init('https://your-fraud-api.railway.app/analyze/');
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    
    $result = curl_exec($ch);
    curl_close($ch);
    
    return json_decode($result, true);
}

// Usage
$result = analyzePhones(['0965842855', '0870123456']);
print_r($result);
?>
```

### **Java**
```java
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;

public class FraudDetectionAPI {
    private static final String API_URL = "https://your-fraud-api.railway.app";
    
    public static String analyzePhones(String[] numbers) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        
        String json = "{\"phone_numbers\": [" + 
                     String.join(",", Arrays.stream(numbers)
                         .map(s -> "\"" + s + "\"")
                         .toArray(String[]::new)) + "]}";
        
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(API_URL + "/analyze/"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(json))
            .build();
            
        HttpResponse<String> response = client.send(request, 
            HttpResponse.BodyHandlers.ofString());
            
        return response.body();
    }
}
```

## 🔒 **Rate Limits & Best Practices**

### **Rate Limits**
- **100 requests per minute** per IP
- **1000 requests per hour** per IP
- Batch requests recommended for multiple items

### **Best Practices**
1. **Batch Processing**: Send multiple items in one request
2. **Cache Results**: Cache responses to reduce API calls
3. **Error Handling**: Always handle HTTP errors and timeouts
4. **Retry Logic**: Implement exponential backoff for retries

### **Error Handling Example**
```javascript
async function safeApiCall(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        return { error: error.message };
    }
}
```

## 📊 **Response Formats**

### **Success Response**
```json
{
  "phone_number": "0965842855",
  "analysis": {
    "phone_head": "096",
    "phone_region": "Vietnam",
    "label": "safe",
    "heading_id": 1
  },
  "fraud_risk": "LOW"
}
```

### **Error Response**
```json
{
  "detail": "Validation error",
  "error_code": 422,
  "message": "Phone number format invalid"
}
```

### **Batch Response**
```json
{
  "summary": {
    "total_analyzed": 3,
    "high_risk_count": 1,
    "low_risk_count": 2,
    "error_count": 0,
    "processing_time": 0.25
  },
  "results": [...]
}
```

## 🆘 **Support & Contact**

- **API Documentation**: `https://your-fraud-api.railway.app/docs`
- **Health Check**: `https://your-fraud-api.railway.app/health`
- **Status Page**: `https://your-fraud-api.railway.app/`

### **Common Issues**
1. **429 Too Many Requests**: Reduce request frequency
2. **422 Validation Error**: Check request format
3. **500 Internal Server Error**: Contact API owner
4. **Timeout**: Implement retry logic

---

## 🎉 **Getting Started**

1. **Test API**: `curl https://your-fraud-api.railway.app/health`
2. **Try Analysis**: Use interactive docs at `/docs`
3. **Integrate**: Use examples above in your application
4. **Monitor**: Check response times and error rates

**Happy coding! 🚀**
