# 🔧 Railway Database Fix Guide

## 🎯 **Vấn Đề**
Railway đã deploy API nhưng database không có tables (no table found).

## 🚀 **Giải Pháp**

### **Method 1: Railway CLI (Recommended)**

#### **Bước 1: Install Railway CLI**
```bash
# Install via npm (nếu có Node.js)
npm install -g @railway/cli

# Hoặc download từ: https://railway.app/cli
```

#### **Bước 2: Login và Connect**
```bash
# Login to Railway
railway login

# Navigate to project folder
cd D:\Projects\Python\FraudDetection

# Link to your Railway project
railway link
# Chọn project: fraud-detection-api
```

#### **Bước 3: Run Migrations**
```bash
# Run database migrations
railway run python database/manage_db.py migrate

# Hoặc sử dụng alembic trực tiếp
railway run alembic upgrade head
```

#### **Bước 4: Populate Phone Headings**
```bash
# Populate phone headings data
railway run python database/manage_db.py populate
```

### **Method 2: Web-based Solution (No CLI needed)**

#### **Bước 1: Tạo Migration Endpoint**
Thêm endpoint vào API để chạy migrations qua web:

```python
# Add to src/main.py
@app.post("/admin/setup-database", summary="Setup database (admin only)")
def setup_database(db: Session = Depends(get_db)):
    """Setup database tables and populate initial data"""
    try:
        # Import here to avoid circular imports
        from alembic.config import Config
        from alembic import command
        import os
        
        # Run migrations
        alembic_cfg = Config("database/alembic.ini")
        alembic_cfg.set_main_option("script_location", "database/alembic")
        command.upgrade(alembic_cfg, "head")
        
        # Populate phone headings
        from .models import PhoneHeading
        count = db.query(PhoneHeading).count()
        
        if count == 0:
            from .populate_headings import populate_phone_headings
            populate_phone_headings()
            
        return {
            "status": "success",
            "message": "Database setup completed",
            "phone_headings_count": db.query(PhoneHeading).count()
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Database setup failed: {str(e)}"
        }
```

#### **Bước 2: Call Setup Endpoint**
```bash
# After deployment, call this once:
curl -X POST "https://your-railway-url.up.railway.app/admin/setup-database"
```

### **Method 3: Fix via Railway Dashboard**

#### **Bước 1: Check Environment Variables**
1. **Railway dashboard → API service → Variables**
2. **Verify `DATABASE_URL` exists:**
   ```
   DATABASE_URL=postgresql://postgres:***@***:5432/railway
   ```

#### **Bước 2: Check PostgreSQL Service**
1. **Click vào PostgreSQL service**
2. **Tab "Metrics" - ensure it's running**
3. **Tab "Connect" - get connection details**

#### **Bước 3: Manual Database Setup**
1. **Connect to database via Railway dashboard:**
   - PostgreSQL service → "Connect" tab
   - Copy connection command
   
2. **Run SQL commands:**
   ```sql
   -- Check if tables exist
   \dt
   
   -- If no tables, create them manually
   -- (Copy from database/alembic/versions/*.py)
   ```

### **Method 4: Reset and Redeploy**

#### **Bước 1: Delete và Recreate PostgreSQL**
1. **Railway dashboard → PostgreSQL service**
2. **Settings → Delete Service**
3. **Add new PostgreSQL service**
4. **Redeploy API service**

#### **Bước 2: Verify Auto-Setup**
- API sẽ tự động tạo tables khi startup
- Auto-populate phone headings nếu database empty

## 🧪 **Testing Database Setup**

### **Test 1: Health Check**
```bash
curl https://your-railway-url/health

# Expected:
{
  "status": "healthy",
  "checks": {
    "database": "healthy"
  }
}
```

### **Test 2: Phone Analysis**
```bash
curl -X POST "https://your-railway-url/analyze/" \
  -H "Content-Type: application/json" \
  -d '{"phone_numbers": ["0965842855"]}'

# Should return analysis results
```

### **Test 3: Database Content**
```bash
# If you have psql installed locally:
psql "postgresql://postgres:password@host:port/railway"

# Check tables:
\dt

# Check phone headings count:
SELECT count(*) FROM phone_headings;
-- Should return 94
```

## 🔧 **Common Issues & Solutions**

### **❌ "relation does not exist"**
**Cause:** Tables not created  
**Solution:** Run migrations (Method 1 or 2)

### **❌ "no phone headings found"**
**Cause:** Database empty  
**Solution:** Run populate command

### **❌ "connection refused"**
**Cause:** Database not running  
**Solution:** Check Railway PostgreSQL service status

### **❌ "permission denied"**
**Cause:** Wrong database credentials  
**Solution:** Check `DATABASE_URL` environment variable

## 📊 **Expected Database Schema**

After successful setup, you should have:

```sql
-- Tables created:
users               -- Phone number records
phone_headings      -- 94 Vietnamese + International prefixes  
sms_scams          -- SMS spam content
banking_scams      -- Scam banking accounts
website_scams      -- Scam websites
alembic_version    -- Migration tracking

-- Data populated:
phone_headings: 94 records (35 safe Vietnamese, 59 unsafe international)
```

## 🎯 **Quick Fix Commands**

### **If you have Railway CLI:**
```bash
# Full database setup in 3 commands:
railway run alembic upgrade head
railway run python database/manage_db.py populate  
railway run python -c "from src.database import test_connection; test_connection()"
```

### **If no Railway CLI:**
```bash
# Use the admin endpoint (add to main.py first):
curl -X POST "https://your-railway-url/admin/setup-database"
```

---

## 🎉 **Success Checklist**

- [ ] ✅ Railway PostgreSQL service running
- [ ] ✅ DATABASE_URL environment variable set
- [ ] ✅ Migrations applied (tables created)
- [ ] ✅ Phone headings populated (94 records)
- [ ] ✅ Health check returns "healthy"
- [ ] ✅ Phone analysis works
- [ ] ✅ API endpoints responding

**🚀 Once database is setup, your API will be fully functional!**
