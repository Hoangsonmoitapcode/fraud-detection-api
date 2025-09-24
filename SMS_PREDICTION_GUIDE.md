# 📱 SMS Spam Prediction với PhoBERT

## 🎯 Tổng quan

Tính năng SMS spam prediction đã được nâng cấp để sử dụng model PhoBERT AI, cho phép phát hiện tin nhắn spam/ham một cách chính xác và thông minh hơn.

## 🚀 Tính năng mới

### ✨ Các endpoint đã được cập nhật:

1. **`/predict-sms/`** (MỚI) - Dự đoán spam/ham bằng AI model
2. **`/check-sms/`** (CẬP NHẬT) - Kiểm tra database + AI fallback
3. API status hiển thị trạng thái PhoBERT model

## 📋 Hướng dẫn sử dụng

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

**Dependencies mới được thêm:**
- `torch>=1.9.0` - PyTorch cho PhoBERT
- `transformers>=4.20.0` - Hugging Face Transformers
- `scikit-learn>=1.0.0` - ML utilities

### 2. Đảm bảo model file có sẵn

Đặt file `phobert_sms_classifier.pkl` trong thư mục root của project.

### 3. Khởi động API

```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Hoặc sử dụng script test:

```bash
python start_and_test.py
```

### 4. Test API

```bash
python test_sms_prediction.py
```

## 🔧 API Endpoints

### 1. AI Prediction Endpoint

**POST `/predict-sms/`**

Dự đoán tin nhắn SMS bằng AI model PhoBERT.

**Request:**
```json
{
  "sms_content": "Chúc mừng! Bạn đã trúng thưởng 100 triệu đồng"
}
```

**Response:**
```json
{
  "sms_content": "Chúc mừng! Bạn đã trúng thưởng 100 triệu đồng",
  "prediction": "spam",
  "confidence": 0.95,
  "risk_level": "HIGH",
  "model_info": {
    "model_type": "PhoBERT",
    "is_loaded": true
  },
  "processed_text": "chúc mừng! bạn đã trúng thưởng 100 triệu đồng"
}
```

### 2. Hybrid Check Endpoint

**GET `/check-sms/`**

Kiểm tra database trước, nếu không tìm thấy sẽ dùng AI model.

**Parameters:**
- `sms_content` (required): Nội dung tin nhắn
- `use_ai_fallback` (optional, default=true): Có dùng AI khi không tìm thấy trong database

**Example:**
```bash
curl "http://localhost:8000/check-sms/?sms_content=Chúc%20mừng%20trúng%20thưởng&use_ai_fallback=true"
```

**Response:**
```json
{
  "sms_content": "Chúc mừng trúng thưởng",
  "is_spam": true,
  "label": "spam",
  "risk_level": "HIGH",
  "match_type": "ai_prediction",
  "confidence": 0.92,
  "source": "ai_model"
}
```

## 🧠 Model Information

### PhoBERT Model
- **Loại**: Vietnamese BERT model
- **Mục đích**: Phân loại tin nhắn SMS thành spam/ham
- **Ngôn ngữ**: Tiếng Việt (chính) + Tiếng Anh
- **Format**: Pickle file (.pkl)

### Confidence Levels
- **HIGH**: confidence >= 0.8
- **MEDIUM**: confidence >= 0.6
- **LOW**: confidence < 0.6

### Risk Levels
- **HIGH**: Spam với confidence cao
- **MEDIUM**: Spam với confidence trung bình
- **LOW**: Ham hoặc spam với confidence thấp

## 🔍 Testing

### Test Cases

1. **Spam tiếng Việt**: "Chúc mừng! Bạn đã trúng thưởng 100 triệu đồng"
2. **Ham tiếng Việt**: "Xin chào, cuộc họp lúc 2pm hôm nay"
3. **Spam tiếng Anh**: "URGENT! Your account will be suspended"
4. **Ham tiếng Anh**: "Thank you for your purchase"

### Chạy test

```bash
# Test cơ bản
python test_sms_prediction.py

# Test với server tự động
python start_and_test.py

# Test với URL khác
python test_sms_prediction.py https://your-api-url.com
```

## 🛠️ Troubleshooting

### Model không load được

1. **Kiểm tra file model:**
   ```bash
   ls -la phobert_sms_classifier.pkl
   ```

2. **Kiểm tra dependencies:**
   ```bash
   pip install torch transformers scikit-learn
   ```

3. **Xem log lỗi:**
   - Model service sẽ log chi tiết lỗi khi load model
   - Kiểm tra console output khi start server

### API không phản hồi

1. **Kiểm tra server đang chạy:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Kiểm tra port:**
   - Đảm bảo port 8000 không bị conflict
   - Thử port khác: `--port 8001`

### Prediction không chính xác

1. **Model có thể cần retrain** với data mới
2. **Kiểm tra preprocessing** - text cần được clean trước khi predict
3. **Confidence thấp** - model không chắc chắn, cần thêm training data

## 📊 Performance

### Response Time
- **Database lookup**: ~10-50ms
- **AI prediction**: ~100-500ms (tùy model size)
- **Hybrid check**: ~10-500ms (tùy source)

### Accuracy
- Phụ thuộc vào chất lượng training data
- Recommend: test với real data để đánh giá

## 🔄 Integration

### Với existing code

```python
import requests

# Sử dụng AI prediction
response = requests.post("http://localhost:8000/predict-sms/", 
                        json={"sms_content": "Your message here"})
result = response.json()

if result["prediction"] == "spam":
    print(f"⚠️ SPAM detected! Confidence: {result['confidence']}")
else:
    print(f"✅ Message is safe")
```

### Với database fallback

```python
# Sử dụng hybrid check (database + AI)
response = requests.get("http://localhost:8000/check-sms/", 
                       params={"sms_content": "Your message", "use_ai_fallback": True})
result = response.json()

print(f"Source: {result['source']}")  # database, ai_model, or none
print(f"Is spam: {result['is_spam']}")
```

## 📈 Monitoring

### Health Check

```bash
curl http://localhost:8000/
```

Kiểm tra:
- ✅ `sms_ai_prediction`: "✅ Active (PhoBERT)"
- Model info trong response

### Logs

Model service sẽ log:
- Model loading status
- Prediction errors
- Performance metrics

## 🚀 Deployment

### Local Development
```bash
python -m uvicorn src.main:app --reload
```

### Production
```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Railway/Cloud
- Đảm bảo `phobert_sms_classifier.pkl` được upload
- Dependencies sẽ tự động install từ `requirements.txt`
- Memory requirements: ít nhất 2GB RAM cho PhoBERT

---

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra logs trong console
2. Test với `test_sms_prediction.py`
3. Verify model file integrity
4. Check API documentation: http://localhost:8000/docs
