# 🎓 Comprehensive Learning Guide - Part 2: FastAPI Application & API Design

## 🚀 **FastAPI Application Structure**

### **File: `src/main.py`**

#### **Application Initialization**
```python
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="🛡️ Fraud Detection API",
    description="Comprehensive fraud detection system...",
    version="3.0.0"
)
```

**Giải thích parameters**:
- **`title`**: Hiển thị trong OpenAPI docs
- **`description`**: Detailed description cho docs
- **`version`**: API versioning, semantic versioning

**Tại sao cần metadata**:
1. **Documentation**: Auto-generated docs với proper info
2. **API discovery**: Clients biết API version và capabilities
3. **Professional**: Production-ready API cần proper metadata

#### **CORS Middleware**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Chi tiết CORS configuration**:
- **`allow_origins=["*"]`**: Allow tất cả origins (development only)
- **`allow_credentials=True`**: Allow cookies/auth headers
- **`allow_methods=["*"]`**: Allow tất cả HTTP methods
- **`allow_headers=["*"]`**: Allow tất cả headers

**Production CORS setup**:
```python
allow_origins=[
    "https://yourdomain.com",
    "https://app.yourdomain.com"
]
```

**Tại sao cần CORS**:
1. **Browser security**: Same-origin policy blocks cross-origin requests
2. **Web client support**: Frontend apps cần call API từ different domain
3. **API accessibility**: Enable web-based API consumers

#### **Database Auto-Setup**
```python
# Tạo bảng (nếu chưa có)
Base.metadata.create_all(bind=engine)

# Auto-populate phone headings on startup
def populate_phone_headings_if_empty():
    try:
        db = SessionLocal()
        from .models import PhoneHeading
        count = db.query(PhoneHeading).count()
        if count == 0:
            print("📱 Database empty - populating phone headings...")
            from .populate_headings import populate_phone_headings
            populate_phone_headings()
            print("✅ Phone headings populated successfully!")
        else:
            print(f"📊 Database already has {count} phone headings")
        db.close()
    except Exception as e:
        print(f"⚠️ Warning: Could not populate phone headings: {e}")
```

**Giải thích auto-setup logic**:
1. **`Base.metadata.create_all()`**: Tạo tất cả tables nếu chưa có
2. **`db.query(PhoneHeading).count()`**: Check xem có data chưa
3. **Conditional population**: Chỉ populate nếu empty
4. **Error handling**: Graceful degradation nếu setup fails

**Tại sao cần auto-setup**:
1. **Railway deployment**: Không có manual setup step
2. **Developer experience**: Clone và run, không cần manual steps
3. **Reliability**: Self-healing, tự setup nếu missing data

#### **Dependency Injection Pattern**
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/analyze/")
def analyze_phone_numbers(
    request: BatchPhoneAnalyze,
    db: Session = Depends(get_db)
):
```

**Giải thích Depends()**:
- **`Depends(get_db)`**: FastAPI dependency injection
- **Automatic execution**: FastAPI tự động call get_db()
- **Cleanup**: finally block đảm bảo db.close()
- **Type hints**: `db: Session` cho IDE support

**Tại sao dùng dependency injection**:
1. **Separation of concerns**: Business logic tách khỏi infrastructure
2. **Testing**: Dễ mock dependencies
3. **Resource management**: Automatic cleanup
4. **Consistency**: Standardized pattern across endpoints

---

## 📊 **API Endpoints Design**

### **Status & Health Endpoints**

#### **API Status Endpoint**
```python
@app.get("/", summary="API Status")
def get_api_status():
    try:
        import psutil
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
    except ImportError:
        cpu_percent = "N/A"
        memory_percent = "N/A"
    
    return {
        "message": "🛡️ Fraud Detection API",
        "version": "3.0.0",
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "uptime_seconds": (datetime.now() - start_time).total_seconds(),
        "system_info": {
            "cpu_usage": f"{cpu_percent}%",
            "memory_usage": f"{memory_percent}%"
        },
        # ... more fields
    }
```

**Giải thích system monitoring**:
- **`psutil.cpu_percent(interval=1)`**: CPU usage over 1 second
- **`psutil.virtual_memory()`**: Memory usage statistics
- **`try/except ImportError`**: Graceful degradation nếu psutil không available
- **`datetime.now().isoformat()`**: ISO 8601 timestamp format

**Tại sao cần system info**:
1. **Monitoring**: Operations team cần biết resource usage
2. **Debugging**: Performance issues correlation
3. **Alerting**: Can setup alerts based on metrics

#### **Health Check Endpoint**
```python
@app.get("/health", summary="Health Check Endpoint")
def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connectivity
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db_status = "healthy"
        db_error = None
    except Exception as e:
        db_status = "degraded"
        db_error = str(e)
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "database": {
            "status": db_status,
            "error": db_error
        },
        "timestamp": datetime.now().isoformat()
    }
```

**Giải thích health check logic**:
- **`text("SELECT 1")`**: Simple query để test connectivity
- **SQLAlchemy 2.0**: Cần wrap raw SQL trong text()
- **Status levels**: "healthy", "degraded", "unhealthy"
- **Error reporting**: Include error message for debugging

**Health check vs Status endpoint**:
- **Health**: Focus on dependencies (database, external services)
- **Status**: Focus on application info và system metrics

### **Phone Analysis Endpoints**

#### **Batch Phone Analysis**
```python
@app.post("/analyze/", summary="Batch Phone Analysis")
def analyze_phone_numbers(
    request: BatchPhoneAnalyze,
    db: Session = Depends(get_db)
):
    results = []
    high_risk_count = 0
    low_risk_count = 0
    error_count = 0
    
    for phone_number in request.phone_numbers:
        try:
            analysis = PhoneService.analyze_phone_number(phone_number, db)
            
            # Create user record
            user = User(
                phone_number=phone_number,
                phone_head=analysis["phone_head"],
                phone_region=analysis["phone_region"],
                label=analysis["label"],
                heading_id=analysis["heading_id"]
            )
            db.add(user)
            
            # Count risk levels
            if analysis["label"] == "unsafe":
                high_risk_count += 1
            else:
                low_risk_count += 1
                
            results.append({
                "phone_number": phone_number,
                "analysis": analysis
            })
            
        except Exception as e:
            error_count += 1
            results.append({
                "phone_number": phone_number,
                "error": str(e)
            })
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        # Handle commit errors
    
    return {
        "results": results,
        "summary": {
            "total_analyzed": len(request.phone_numbers),
            "high_risk_count": high_risk_count,
            "low_risk_count": low_risk_count,
            "error_count": error_count,
            "processing_time": f"{(datetime.now() - start_time).total_seconds():.3f}s"
        }
    }
```

**Giải thích batch processing logic**:
1. **Loop through inputs**: Process từng phone number
2. **Error isolation**: 1 phone fail không affect others
3. **Database transaction**: Batch commit cho performance
4. **Rollback on error**: Data consistency
5. **Summary statistics**: Overview của batch processing

**Tại sao dùng batch processing**:
1. **Performance**: 1 API call thay vì N calls
2. **Atomic operations**: All-or-nothing database commits
3. **Reduced overhead**: Fewer HTTP requests
4. **Better UX**: Bulk operations cho users

#### **User Record Creation**
```python
user = User(
    phone_number=phone_number,
    phone_head=analysis["phone_head"],
    phone_region=analysis["phone_region"],
    label=analysis["label"],
    heading_id=analysis["heading_id"]
)
db.add(user)
```

**Tại sao lưu user records**:
1. **Analytics**: Track usage patterns
2. **Audit trail**: Who analyzed what và when
3. **Machine learning**: Data for future model training
4. **Compliance**: Regulatory requirements

### **Scam Detection Endpoints**

#### **SMS Scam Detection**
```python
@app.post("/sms-scam/", summary="SMS Scam Detection")
def detect_sms_scam(request: SmsScamCreate, db: Session = Depends(get_db)):
    # Define scam patterns
    scam_patterns = [
        r'trúng thưởng',
        r'click.*link',
        r'chúc mừng.*triệu',
        r'nhận ngay',
        r'khuyến mãi.*%',
        r'miễn phí.*gọi',
        r'tặng.*xu',
        r'quà.*tặng',
        # ... more patterns
    ]
    
    detected_patterns = []
    risk_score = 0
    
    message_lower = request.message.lower()
    
    for pattern in scam_patterns:
        if re.search(pattern, message_lower):
            detected_patterns.append(pattern)
            risk_score += 10
    
    # Determine risk level
    if risk_score >= 30:
        risk_level = "high"
    elif risk_score >= 10:
        risk_level = "medium"
    else:
        risk_level = "low"
    
    analysis_result = {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "detected_patterns": detected_patterns,
        "total_patterns": len(detected_patterns),
        "message_length": len(request.message),
        "analysis_timestamp": datetime.now().isoformat()
    }
    
    # Save to database
    sms_scam = SmsScam(
        message=request.message,
        risk_level=risk_level,
        detected_patterns=",".join(detected_patterns),
        analysis_result=str(analysis_result)
    )
    db.add(sms_scam)
    db.commit()
    
    return analysis_result
```

**Giải thích SMS scam detection**:
1. **Pattern matching**: Regex patterns cho common scam phrases
2. **Risk scoring**: Accumulate score based on matched patterns
3. **Risk levels**: Categorize into high/medium/low
4. **Vietnamese language**: Patterns specific to Vietnamese scams

**Tại sao dùng regex patterns**:
1. **Flexibility**: Có thể match variations of phrases
2. **Performance**: Fast pattern matching
3. **Maintainability**: Easy to add/remove patterns
4. **Language specific**: Tailored for Vietnamese scam tactics

**Risk scoring algorithm**:
- **Each pattern**: +10 points
- **Thresholds**: 30+ high, 10+ medium, <10 low
- **Rationale**: Multiple patterns indicate higher risk

#### **Banking Scam Detection**
```python
@app.post("/banking-scam/", summary="Banking Scam Detection")
def detect_banking_scam(request: BankingScamCreate, db: Session = Depends(get_db)):
    banking_scam_patterns = [
        r'vietcombank.*khuyến mãi',
        r'techcombank.*ưu đãi',
        r'bidv.*tặng',
        r'agribank.*miễn phí',
        r'sacombank.*lãi suất',
        r'mb.*bank.*quà',
        r'acb.*thưởng',
        r'vpbank.*khuyến mãi',
        r'tpbank.*ưu đãi',
        r'hdbank.*tặng',
        r'ocb.*miễn phí',
        r'shb.*lãi suất',
        r'eximbank.*quà',
        r'namabank.*thưởng',
        r'pgbank.*khuyến mãi',
        r'seabank.*ưu đãi',
        r'lienvietpostbank.*tặng',
        r'kienlongbank.*miễn phí',
        r'bacabank.*lãi suất',
        r'oceanbank.*quà'
    ]
    # ... similar logic to SMS
```

**Banking-specific patterns**:
- **Bank names**: All major Vietnamese banks
- **Common tactics**: Fake promotions, interest rates, gifts
- **Phishing indicators**: Urgent action, too-good-to-be-true offers

---

## 📋 **Data Schemas & Validation**

### **File: `src/schemas.py`**

#### **Pydantic Models**
```python
from pydantic import BaseModel, validator
from typing import List, Optional

class BatchPhoneAnalyze(BaseModel):
    phone_numbers: List[str]
    
    @validator('phone_numbers')
    def validate_phone_numbers(cls, v):
        if not v:
            raise ValueError('Phone numbers list cannot be empty')
        if len(v) > 100:
            raise ValueError('Cannot analyze more than 100 phone numbers at once')
        return v
```

**Giải thích Pydantic validation**:
- **`BaseModel`**: Base class cho all Pydantic models
- **`List[str]`**: Type hint, list of strings
- **`@validator`**: Custom validation decorator
- **`cls`**: Class method, access to class
- **`v`**: Value being validated

**Tại sao dùng Pydantic**:
1. **Type safety**: Runtime type checking
2. **Automatic validation**: FastAPI integration
3. **Serialization**: JSON to Python objects
4. **Documentation**: Auto-generate OpenAPI schemas

#### **Response Models**
```python
class UserResponse(BaseModel):
    id: int
    phone_number: str
    phone_head: str
    phone_region: str
    label: Optional[str]
    heading_id: Optional[int]
    
    class Config:
        from_attributes = True
```

**Config class explanation**:
- **`from_attributes = True`**: Allow creation from ORM objects
- **Pydantic v2**: Replaces `orm_mode = True` from v1
- **ORM integration**: Convert SQLAlchemy objects to Pydantic

#### **Custom Validators**
```python
@validator('phone_numbers')
def validate_phone_numbers(cls, v):
    if not v:
        raise ValueError('Phone numbers list cannot be empty')
    if len(v) > 100:
        raise ValueError('Cannot analyze more than 100 phone numbers at once')
    
    # Validate each phone number
    for phone in v:
        if not isinstance(phone, str):
            raise ValueError('All phone numbers must be strings')
        if len(phone) < 5:
            raise ValueError(f'Phone number too short: {phone}')
        if len(phone) > 20:
            raise ValueError(f'Phone number too long: {phone}')
    
    return v
```

**Validation logic**:
1. **Empty check**: Prevent empty requests
2. **Batch size limit**: Prevent overload (100 max)
3. **Type checking**: Ensure strings
4. **Length validation**: Reasonable phone number lengths

---

*Tiếp tục với Part 3...*
