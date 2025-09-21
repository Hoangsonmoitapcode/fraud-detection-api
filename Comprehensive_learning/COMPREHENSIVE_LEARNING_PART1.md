# 🎓 Comprehensive Learning Guide - Part 1: Architecture & Core Concepts

## 📋 **Mục đích của file này**

File này giải thích **CHI TIẾT** tất cả mọi tính năng, hàm, thư viện, cú pháp được sử dụng trong project. Mục đích để bạn hiểu **TẠI SAO** và **NHƯ THẾ NÀO** mọi thứ hoạt động.

---

## 🏗️ **Kiến trúc tổng quan**

### **Tại sao chọn FastAPI?**
```python
from fastapi import FastAPI
```

**FastAPI** được chọn vì:
1. **Performance cao**: Nhanh nhất trong các Python web frameworks
2. **Type hints**: Tự động validation với Python type hints
3. **Auto documentation**: Tự động tạo OpenAPI/Swagger docs
4. **Async support**: Native async/await support
5. **Modern**: Built for Python 3.6+ với modern features

**So sánh với alternatives**:
- **Flask**: Đơn giản hơn nhưng thiếu features, cần thêm extensions
- **Django**: Quá nặng cho API, built-in ORM không flexible
- **FastAPI**: Perfect balance giữa performance và features

### **Tại sao chọn SQLAlchemy?**
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
```

**SQLAlchemy** được chọn vì:
1. **ORM powerful**: Object-Relational Mapping mạnh nhất Python
2. **Database agnostic**: Hoạt động với PostgreSQL, MySQL, SQLite, etc.
3. **Connection pooling**: Quản lý connections hiệu quả
4. **Migration support**: Tích hợp với Alembic
5. **Query optimization**: Lazy loading, eager loading, query optimization

**Alternatives bị loại**:
- **Django ORM**: Chỉ dùng với Django framework
- **Peewee**: Đơn giản hơn nhưng thiếu advanced features
- **Raw SQL**: Không có type safety, khó maintain

---

## 🗄️ **Database Design & Models**

### **File: `src/models.py`**

#### **Base Model Pattern**
```python
from .database import Base

class PhoneHeading(Base):
    __tablename__ = "phone_headings"
```

**Giải thích**:
- **`Base`**: SQLAlchemy declarative base, tất cả models inherit từ đây
- **`__tablename__`**: Tên table trong database, convention là snake_case
- **Tại sao dùng ORM**: Type safety, relationship management, query builder

#### **Column Definitions**
```python
id = Column(Integer, primary_key=True, index=True)
heading = Column(String, nullable=False, unique=True)
region = Column(String, nullable=False)
status = Column(String, nullable=False)
```

**Chi tiết từng parameter**:
- **`Integer`**: SQLAlchemy type mapping to database INTEGER
- **`primary_key=True`**: Đánh dấu primary key, auto-increment
- **`index=True`**: Tạo database index cho faster queries
- **`String`**: VARCHAR type, flexible length
- **`nullable=False`**: NOT NULL constraint
- **`unique=True`**: UNIQUE constraint, prevent duplicates

**Tại sao không dùng `VARCHAR(50)`**:
- **Flexibility**: String length có thể thay đổi
- **PostgreSQL**: VARCHAR và TEXT performance tương tự
- **Maintenance**: Không cần alter table khi cần longer strings

#### **Relationships**
```python
# Trong PhoneHeading
users = relationship("User", back_populates="heading_info")

# Trong User  
heading_id = Column(Integer, ForeignKey("phone_headings.id"), nullable=True)
heading_info = relationship("PhoneHeading", back_populates="users")
```

**Giải thích Relationship**:
- **`relationship()`**: SQLAlchemy ORM relationship, không tạo column
- **`back_populates`**: Bidirectional relationship
- **`ForeignKey`**: Database foreign key constraint
- **`nullable=True`**: Allow NULL (không phải tất cả phone numbers đều có trong database)

**Tại sao dùng bidirectional relationship**:
- **Navigation**: Có thể query từ cả 2 directions
- **Lazy loading**: SQLAlchemy chỉ load khi cần
- **Data consistency**: Đảm bảo data integrity

---

## 🔧 **Database Configuration**

### **File: `src/database.py`**

#### **Connection String với Environment Variables**
```python
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+psycopg2://fastapi_user:mypassword@localhost:5432/fastapi_db"
)
```

**Giải thích chi tiết**:
- **`os.getenv()`**: Lấy environment variable, fallback to default
- **`postgresql+psycopg2://`**: SQLAlchemy dialect + driver
- **`fastapi_user:mypassword`**: Username và password
- **`localhost:5432`**: Host và port (PostgreSQL default port)
- **`fastapi_db`**: Database name

**Tại sao dùng environment variables**:
1. **Security**: Không hardcode credentials trong code
2. **Flexibility**: Different environments (dev/staging/prod)
3. **Railway compatibility**: Railway auto-injects DATABASE_URL

#### **Connection Pooling**
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    echo=False
)
```

**Chi tiết từng parameter**:
- **`pool_size=5`**: 5 persistent connections trong pool
- **`max_overflow=10`**: Tối đa 10 connections thêm khi cần
- **`pool_timeout=30`**: 30 seconds timeout khi get connection
- **`pool_recycle=3600`**: Recycle connections sau 1 hour (tránh stale connections)
- **`echo=False`**: Không log SQL queries (set True để debug)

**Tại sao cần connection pooling**:
1. **Performance**: Tái sử dụng connections, không tạo mới mỗi request
2. **Resource management**: Limit số connections to database
3. **Reliability**: Handle connection failures gracefully

#### **Session Management**
```python
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Giải thích pattern**:
- **`sessionmaker`**: Factory để tạo database sessions
- **`bind=engine`**: Bind session với database engine
- **`yield`**: Generator pattern, FastAPI dependency injection
- **`try/finally`**: Đảm bảo session được close dù có exception

**Tại sao dùng dependency injection**:
1. **Automatic cleanup**: Session tự động close sau request
2. **Testing**: Dễ mock database trong tests
3. **Consistency**: Mỗi request có session riêng

---

## 📱 **Phone Service Logic**

### **File: `src/phone_service.py`**

#### **Phone Number Parsing**
```python
def extract_phone_head(phone_number: str) -> str:
    # Remove spaces and special characters except +
    cleaned = re.sub(r'[^\d+]', '', phone_number)
```

**Giải thích regex `r'[^\d+]'`**:
- **`r''`**: Raw string, không escape backslashes
- **`[^\d+]`**: Character class, match anything KHÔNG phải digit hoặc +
- **`\d`**: Shorthand for [0-9]
- **`^` inside []**: Negation, nghĩa là NOT
- **Result**: Xóa tất cả except digits và +

**Tại sao dùng regex thay vì string methods**:
1. **Concise**: 1 line thay vì multiple replace() calls
2. **Performance**: Compiled regex nhanh hơn
3. **Flexibility**: Dễ modify pattern

#### **International Format Detection**
```python
if cleaned.startswith('+'):
    # Single digit: +1, +7
    if re.match(r'^\+[17]', cleaned):
        return cleaned[:2]
    # Two digits: +44, +49, +33, etc.
    elif re.match(r'^\+(?:44|49|33|39|34|81|82|86|91|98|92|94|95|90|66|65|60|62|63|84|20|27|55|52|61)', cleaned):
        return cleaned[:3]
```

**Giải thích regex patterns**:
- **`r'^\+[17]'`**: 
  - `^`: Start of string
  - `\+`: Literal + character (escaped)
  - `[17]`: Character class, match 1 OR 7
- **`r'^\+(?:44|49|33|...)'`**:
  - `(?:...)`: Non-capturing group
  - `44|49|33`: Alternation, match any of these
  - `cleaned[:3]`: Slice first 3 characters

**Tại sao hardcode country codes**:
1. **Performance**: Faster than database lookup
2. **Reliability**: No external dependencies
3. **Common cases**: Cover 95% of international numbers

#### **Vietnamese Mobile Detection**
```python
vietnam_mobile_safe = [
    '096', '097', '098', '032', '033', '034', '035', '036', '037', '038', '039',
    '070', '076', '077', '078', '079', '081', '082', '083', '084', '085', '088',
    '091', '094', '087', '092', '056', '058', '099', '089', '059', '090', '093', '095'
]
```

**Tại sao dùng list thay vì set**:
- **List**: Ordered, dễ đọc, nhóm theo carrier
- **Set**: Faster lookup nhưng không cần vì list nhỏ
- **Performance**: 33 items, linear search vẫn nhanh

**Carrier grouping logic**:
```python
# Viettel: 032-039, 096-098
# Vinaphone: 081-085, 088, 091, 094  
# MobiFone: 070, 076-079
# iTel: 087
# Vietnamobile: 092, 056, 058
# Wintel: 099
# VNPAY Sky: 089
```

#### **Landline Regional Mapping**
```python
vietnam_landline_unsafe = {
    '024': 'Hà Nội',           # Hanoi
    '028': 'TP.HCM',          # Ho Chi Minh City
    '025': 'Hải Phòng',       # Hai Phong
    # ... 80+ entries
}
```

**Tại sao dùng dictionary**:
- **O(1) lookup**: Hash table, constant time
- **Key-value mapping**: Natural fit cho prefix → region
- **Memory efficient**: Chỉ store cần thiết

**Regional information format**:
```python
if phone_head in vietnam_landline_unsafe:
    region = f"Vietnam - {vietnam_landline_unsafe[phone_head]}"
    return region, "unsafe", None
```

**Tại sao landline = unsafe**:
1. **Spoofing risk**: Dễ fake caller ID
2. **No 2FA**: Không có SMS verification
3. **Scammer preference**: Thường dùng landline numbers

---

*Tiếp tục với Part 2...*
