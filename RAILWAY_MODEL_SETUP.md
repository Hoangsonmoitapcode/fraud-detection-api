# 🚂 Railway Deployment với PhoBERT Model

## ⚠️ Vấn đề với File Model Lớn

File `phobert_sms_classifier.pkl` (518MB) quá lớn để push lên GitHub. Railway cần file này để SMS prediction hoạt động.

## 🔧 Giải pháp Deployment

### Phương án 1: Upload Model qua Railway CLI (Khuyến nghị)

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login và connect project**:
   ```bash
   railway login
   railway link [your-project-id]
   ```

3. **Upload model file**:
   ```bash
   railway up --detach
   ```

### Phương án 2: Environment Variables để Download Model

Thêm vào Railway environment variables:

```env
MODEL_DOWNLOAD_URL=https://your-storage-url.com/phobert_sms_classifier.pkl
MODEL_AUTO_DOWNLOAD=true
```

Cập nhật `src/sms_prediction_service.py`:

```python
import os
import requests

def download_model_if_needed(self):
    if not os.path.exists(self.model_path):
        download_url = os.getenv("MODEL_DOWNLOAD_URL")
        if download_url:
            print("📥 Downloading model from remote...")
            response = requests.get(download_url)
            with open(self.model_path, 'wb') as f:
                f.write(response.content)
            print("✅ Model downloaded successfully")
```

### Phương án 3: Google Drive/Dropbox Link

1. Upload model lên Google Drive/Dropbox
2. Tạo public download link
3. Sử dụng startup script để download

### Phương án 4: Railway Volume (Pro Plan)

```bash
railway volume create model-storage
railway volume mount model-storage /app/models
```

## 🔄 Kiểm tra Deployment

Sau khi deploy, kiểm tra:

1. **API Status**:
   ```bash
   curl https://your-railway-app.railway.app/
   ```

2. **Model Status**:
   ```bash
   curl https://your-railway-app.railway.app/predict-sms/ \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{"sms_content": "Test message"}'
   ```

3. **Logs**:
   ```bash
   railway logs
   ```

## 📊 Memory Requirements

- **Minimum**: 2GB RAM
- **Recommended**: 4GB RAM
- **Storage**: 1GB+ (cho model + dependencies)

## 🚨 Fallback Strategy

Nếu model không load được, API sẽ:
- Fallback về database lookup
- Trả về prediction = "unknown" với confidence = 0.0
- Vẫn hoạt động bình thường với các tính năng khác

## 🔧 Troubleshooting

### Model không load được:
```bash
railway logs | grep "SMS"
```

### Memory issues:
- Upgrade Railway plan
- Optimize model size
- Implement lazy loading

### Network timeout:
- Increase download timeout
- Use CDN for model hosting
- Split model thành chunks nhỏ hơn

## 📝 Notes

- File model đã được add vào `.gitignore`
- API sẽ hoạt động mà không cần model (fallback mode)
- Cần setup model riêng cho production environment
