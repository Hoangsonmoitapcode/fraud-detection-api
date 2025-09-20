# 🚀 Deployment Steps - Railway via GitHub

## 📋 **Hướng Dẫn Deploy Chi Tiết**

### **Bước 1: ✅ Hoàn thành - Chuẩn bị code**
- Git repository đã được khởi tạo
- Code đã được commit
- Tất cả files deployment đã sẵn sàng

### **Bước 2: Tạo GitHub Repository**

1. **Truy cập GitHub.com và đăng nhập**
2. **Tạo repository mới:**
   - Click "New repository"
   - Repository name: `fraud-detection-api` (hoặc tên bạn muốn)
   - Description: `Fraud Detection API with Vietnamese carriers support`
   - Chọn **Public** (để Railway có thể truy cập)
   - **KHÔNG** check "Initialize with README" (vì đã có code)
   - Click "Create repository"

3. **Push code lên GitHub:**
   ```bash
   # Thay YOUR_USERNAME bằng username GitHub của bạn
   git remote add origin https://github.com/YOUR_USERNAME/fraud-detection-api.git
   git branch -M main
   git push -u origin main
   ```

### **Bước 3: Deploy lên Railway**

1. **Truy cập Railway.app:**
   - Mở https://railway.app
   - Click "Login" → "Login with GitHub"
   - Authorize Railway truy cập GitHub

2. **Tạo project mới:**
   - Click "New Project"
   - Chọn "Deploy from GitHub repo"
   - Chọn repository `fraud-detection-api` vừa tạo
   - Click "Deploy Now"

3. **Thêm PostgreSQL Database:**
   - Trong project dashboard, click "New"
   - Chọn "Database" → "Add PostgreSQL"
   - Database sẽ được tạo tự động

4. **Cấu hình Environment Variables:**
   - Click vào service "fraud-detection-api"
   - Vào tab "Variables"
   - Railway sẽ tự động set `DATABASE_URL` từ PostgreSQL
   - Thêm biến: `PORT=8000` (nếu cần)

### **Bước 4: Chờ deployment hoàn thành**

- Railway sẽ tự động:
  - Build Docker container
  - Install dependencies từ `requirements.txt`
  - Chạy migrations
  - Start server với `Procfile`

- Thời gian: 3-5 phút

### **Bước 5: Lấy URL của API**

1. **Trong Railway dashboard:**
   - Click vào service name
   - Vào tab "Settings"
   - Scroll xuống "Domains"
   - Copy URL (dạng: `https://fraud-detection-api-production-xxxx.up.railway.app`)

2. **Test API:**
   ```bash
   # Thay YOUR_URL bằng URL thực
   curl https://your-api-url.up.railway.app/health
   ```

## 🎯 **Sau khi Deploy thành công**

### **URL của bạn sẽ có dạng:**
```
https://fraud-detection-api-production-1234.up.railway.app
```

### **Test các endpoints:**

```bash
# Health check
curl https://your-url/health

# API status
curl https://your-url/

# Phone analysis
curl -X POST "https://your-url/analyze/" \
  -H "Content-Type: application/json" \
  -d '{"phone_numbers": ["0965842855", "0870123456"]}'

# Interactive docs
# Mở browser: https://your-url/docs
```

## 👥 **Users CỦA BẠN SẼ SỬ DỤNG NHƯ SAO?**

### ✅ **Users KHÔNG cần cài gì cả!**

Users chỉ cần:
1. **Internet connection**
2. **Programming language** (JavaScript, Python, PHP, Java, etc.)
3. **Your API URL**

### **Ví dụ users sử dụng:**

#### **JavaScript (Web/Node.js):**
```javascript
// Analyze phone numbers
const response = await fetch('https://your-url/analyze/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        phone_numbers: ['0965842855', '0870123456', '0920123456']
    })
});
const data = await response.json();
console.log(data);
```

#### **Python:**
```python
import requests

# Users chỉ cần requests library
response = requests.post('https://your-url/analyze/', 
                        json={'phone_numbers': ['0965842855']})
result = response.json()
print(result)
```

#### **PHP:**
```php
<?php
$data = json_encode(['phone_numbers' => ['0965842855']]);
$ch = curl_init('https://your-url/analyze/');
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$result = curl_exec($ch);
curl_close($ch);
echo $result;
?>
```

#### **cURL (Command line):**
```bash
curl -X POST "https://your-url/analyze/" \
  -H "Content-Type: application/json" \
  -d '{"phone_numbers": ["0965842855"]}'
```

## 📱 **Cách Chia Sẻ API với Users**

### **1. Cung cấp thông tin cơ bản:**
```
🛡️ Fraud Detection API
📍 URL: https://your-api-url.up.railway.app
📚 Docs: https://your-api-url.up.railway.app/docs
🏥 Health: https://your-api-url.up.railway.app/health
```

### **2. Gửi file hướng dẫn:**
- `API_USAGE_GUIDE.md` - Complete guide
- Examples cho từng programming language

### **3. Demo endpoints:**
- Interactive documentation: `/docs`
- Test ngay trên browser

## 🔧 **Troubleshooting**

### **Nếu deployment fail:**

1. **Check logs:**
   - Railway dashboard → Service → "Deployments" tab
   - Click vào deployment để xem logs

2. **Common issues:**
   - Missing dependencies: Check `requirements.txt`
   - Database connection: Check `DATABASE_URL` variable
   - Port issues: Ensure using `$PORT` environment variable

3. **Fix và redeploy:**
   - Fix code locally
   - `git add . && git commit -m "Fix deployment"`
   - `git push origin main`
   - Railway sẽ tự động redeploy

## 💰 **Cost & Limits**

### **Railway Free Tier:**
- **$5 credit per month** (free)
- **500 hours execution time**
- **1GB RAM**
- **1GB storage**
- **Shared CPU**

### **Upgrade nếu cần:**
- **Pro Plan**: $20/month
- **More resources và priority**

## 🎉 **Success Checklist**

- [ ] ✅ Code pushed to GitHub
- [ ] ✅ Railway project created
- [ ] ✅ PostgreSQL database added
- [ ] ✅ Deployment successful
- [ ] ✅ API URL accessible
- [ ] ✅ Health check returns 200
- [ ] ✅ Phone analysis working
- [ ] ✅ Interactive docs available
- [ ] ✅ All endpoints responding

---

## 🚀 **Ready to Go!**

Sau khi hoàn thành các bước trên, bạn sẽ có:

1. **✅ Public API URL** - Accessible từ anywhere
2. **✅ PostgreSQL Database** - Hosted trên Railway
3. **✅ Auto-scaling** - Railway handle traffic
4. **✅ HTTPS Security** - SSL certificate tự động
5. **✅ Monitoring** - Built-in logs và metrics

**Users của bạn chỉ cần biết API URL và có thể sử dụng ngay!**
