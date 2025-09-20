# 🗄️ Railway PostgreSQL Setup Guide

## 🎯 **Tổng Quan**
Hướng dẫn chi tiết cách thêm PostgreSQL database vào Railway project và cấu hình kết nối.

## 🚀 **Step-by-Step Setup**

### **Bước 1: Deploy API lên Railway**

1. **Truy cập Railway:**
   - Mở https://railway.app
   - Click **"Login"** → **"Login with GitHub"**
   - Authorize Railway access

2. **Tạo Project:**
   - Click **"New Project"**
   - Chọn **"Deploy from GitHub repo"**
   - Tìm repository: **`Hoangsonmoitapcode/fraud-detection-api`**
   - Click **"Deploy Now"**

3. **Đợi Initial Deployment:**
   - Railway sẽ build code (2-3 phút)
   - Status sẽ hiển thị "Building..." → "Deployed"

### **Bước 2: Thêm PostgreSQL Database**

#### **Option A: Từ Project Dashboard**
1. **Trong Railway dashboard:**
   - Click **"New"** (nút + ở góc phải)
   - Chọn **"Database"**
   - Click **"Add PostgreSQL"**

#### **Option B: Từ Service Settings**
1. **Click vào API service name**
2. **Tab "Settings"**
3. **Scroll xuống "Connected Services"**
4. **Click "Connect" → "New PostgreSQL"**

### **Bước 3: Database sẽ được tạo tự động**

Railway sẽ:
- ✅ Tạo PostgreSQL instance
- ✅ Generate database credentials
- ✅ Tự động set `DATABASE_URL` environment variable
- ✅ Connect database với API service

### **Bước 4: Verify Database Connection**

1. **Check Environment Variables:**
   - Click vào API service
   - Tab **"Variables"**
   - Xem `DATABASE_URL` đã được set chưa (dạng: `postgresql://username:password@host:port/database`)

2. **Check Deployment Logs:**
   - Tab **"Deployments"**
   - Click vào latest deployment
   - Xem logs để confirm database connection

### **Bước 5: Run Database Migrations**

Railway sẽ tự động chạy migrations khi deploy, nhưng nếu cần manual:

1. **Trong Railway dashboard:**
   - Click vào API service
   - Tab **"Settings"** → **"Environment"**
   - Add variable: `RUN_MIGRATIONS=true`

2. **Hoặc connect qua Railway CLI:**
   ```bash
   # Install Railway CLI (nếu có npm)
   npm install -g @railway/cli
   
   # Login và connect
   railway login
   railway link
   
   # Run migrations
   railway run python database/manage_db.py migrate
   ```

### **Bước 6: Populate Phone Headings Data**

**Option A: Automatic (Recommended)**
- Thêm vào `src/main.py` startup event:
```python
@app.on_event("startup")
async def startup_event():
    # Auto-populate phone headings if empty
    db = SessionLocal()
    try:
        count = db.query(PhoneHeading).count()
        if count == 0:
            from .populate_headings import populate_phone_headings
            populate_phone_headings()
    finally:
        db.close()
```

**Option B: Manual via Railway CLI**
```bash
railway run python -c "from src.populate_headings import populate_phone_headings; populate_phone_headings()"
```

## 🔧 **Troubleshooting**

### **❌ "Database connection failed"**

#### **Check 1: Environment Variables**
```bash
# Trong Railway dashboard → Variables
DATABASE_URL=postgresql://postgres:password@host:port/railway
```

#### **Check 2: Database Status**
```bash
# Railway dashboard → PostgreSQL service
# Status should be "Running"
# Check resource usage
```

#### **Check 3: Network Connectivity**
```bash
# Railway logs should show:
# "✅ Database connection successful!"
# "📊 Connected to: host:port/database"
```

### **❌ "Migration failed"**

#### **Solution 1: Manual Migration**
```bash
# Railway CLI
railway run alembic upgrade head
```

#### **Solution 2: Reset Database**
```bash
# ⚠️ CẢNH BÁO: Sẽ xóa tất cả data
railway run alembic downgrade base
railway run alembic upgrade head
```

### **❌ "Empty phone headings"**

#### **Solution: Populate Data**
```bash
# Via Railway CLI
railway run python database/manage_db.py populate

# Hoặc add startup event (recommended)
```

## 📊 **Database Configuration Details**

### **Railway PostgreSQL Specs:**
- **Version**: PostgreSQL 15
- **Storage**: 1GB (free tier)
- **Connections**: 100 concurrent
- **Backup**: Daily automatic backups
- **SSL**: Enabled by default

### **Environment Variables Auto-Generated:**
```bash
DATABASE_URL=postgresql://postgres:password@host:port/railway
PGHOST=host
PGPORT=port  
PGUSER=postgres
PGPASSWORD=password
PGDATABASE=railway
```

### **Connection Pool Settings:**
```python
# src/database.py - Already configured
engine = create_engine(
    DATABASE_URL,
    pool_size=5,          # 5 persistent connections
    max_overflow=10,      # 10 additional when needed
    pool_timeout=30,      # 30s connection timeout
    pool_recycle=3600     # Recycle connections every hour
)
```

## 🧪 **Testing Database Connection**

### **Method 1: Health Check Endpoint**
```bash
# After deployment
curl https://your-railway-url.up.railway.app/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2025-09-20T...",
  "checks": {
    "database": "healthy",
    "api": "healthy"
  }
}
```

### **Method 2: API Status Endpoint**
```bash
curl https://your-railway-url.up.railway.app/

# Should show system info without errors
```

### **Method 3: Phone Analysis Test**
```bash
curl -X POST "https://your-railway-url.up.railway.app/analyze/" \
  -H "Content-Type: application/json" \
  -d '{"phone_numbers": ["0965842855"]}'

# Should return analysis results
```

## 📈 **Database Monitoring**

### **Railway Dashboard:**
1. **Click vào PostgreSQL service**
2. **Tab "Metrics":**
   - CPU usage
   - Memory usage
   - Storage usage
   - Connection count

3. **Tab "Logs":**
   - Database startup logs
   - Connection logs
   - Query logs (if enabled)

### **Custom Monitoring:**
```python
# Add to health check endpoint
def get_database_stats(db: Session):
    try:
        # Connection count
        result = db.execute(text("SELECT count(*) FROM pg_stat_activity"))
        connections = result.scalar()
        
        # Database size
        result = db.execute(text("SELECT pg_size_pretty(pg_database_size(current_database()))"))
        db_size = result.scalar()
        
        return {
            "connections": connections,
            "database_size": db_size,
            "status": "healthy"
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

## 💰 **Cost & Limits**

### **Railway Free Tier:**
- **PostgreSQL**: 1GB storage
- **Connections**: 100 concurrent
- **Backup**: 7 days retention
- **Uptime**: 99.9% SLA

### **Upgrade Options:**
- **Pro Plan**: $20/month
  - 8GB storage
  - 500 connections
  - 30 days backup retention
  - Priority support

## 🔄 **Database Management**

### **Backup Strategy:**
```bash
# Railway automatic backups (daily)
# Manual backup via Railway CLI:
railway run pg_dump $DATABASE_URL > backup.sql
```

### **Restore Process:**
```bash
# Restore from backup
railway run psql $DATABASE_URL < backup.sql
```

### **Migration Management:**
```bash
# Create new migration
railway run alembic revision --autogenerate -m "description"

# Apply migrations
railway run alembic upgrade head

# Check migration status
railway run alembic current
```

## 🎯 **Success Indicators**

### **✅ Database Setup Successful When:**
- Railway dashboard shows PostgreSQL service "Running"
- `DATABASE_URL` environment variable is set
- API health check returns "healthy"
- Phone analysis endpoints work
- No database connection errors in logs

### **📊 Expected Database Contents:**
```sql
-- After successful setup:
SELECT 'phone_headings' as table_name, count(*) as count FROM phone_headings
UNION
SELECT 'users', count(*) FROM users  
UNION
SELECT 'sms_scams', count(*) FROM sms_scams
UNION
SELECT 'banking_scams', count(*) FROM banking_scams
UNION
SELECT 'website_scams', count(*) FROM website_scams;

-- Expected results:
-- phone_headings: 94 (all Vietnamese + International)
-- Other tables: 0 (initially empty)
```

## 🔒 **Security Best Practices**

### **1. Environment Variables:**
- Railway auto-generates secure credentials
- Never hardcode database URLs
- Use Railway's built-in secret management

### **2. Connection Security:**
- SSL enabled by default
- Encrypted connections
- Network isolation

### **3. Access Control:**
- Only Railway services can access database
- No public internet access
- Firewall protection

---

## 🎉 **Ready to Deploy!**

**Sau khi hoàn thành setup PostgreSQL:**

1. ✅ **Database Running**: Railway PostgreSQL service active
2. ✅ **Auto-Connected**: `DATABASE_URL` environment variable set
3. ✅ **Migrations Applied**: All tables created
4. ✅ **Data Populated**: 94 phone headings loaded
5. ✅ **Health Check**: API returns "healthy"

**🚀 Your Fraud Detection API will be fully operational with centralized database!**

---

*📝 Note: Railway makes database setup incredibly easy - most steps are automatic!*
