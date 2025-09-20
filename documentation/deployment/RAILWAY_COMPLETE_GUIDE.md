# 🚂 Railway Deployment - Complete Guide

## 🎯 **Overview**

This guide covers the complete deployment process for the Fraud Detection API on Railway platform, including database setup, environment configuration, and troubleshooting.

---

## 🚀 **Quick Deployment**

### **Prerequisites**
- GitHub account
- Railway account (free tier available)
- Git installed locally

### **Step 1: Repository Setup**
```bash
# Clone or fork the repository
git clone https://github.com/Hoangsonmoitapcode/fraud-detection-api.git
cd fraud-detection-api

# Push to your GitHub repository
git remote set-url origin https://github.com/YOUR_USERNAME/fraud-detection-api.git
git push -u origin main
```

### **Step 2: Railway Project Creation**
1. Visit [railway.app](https://railway.app)
2. **Login** with GitHub
3. **New Project** → **Deploy from GitHub repo**
4. **Select** your forked repository
5. **Deploy** automatically starts

### **Step 3: Database Setup**
1. **Add PostgreSQL** service to project
2. **Connect** services in Railway dashboard
3. **Environment variables** auto-configured

---

## 🔧 **Detailed Configuration**

### **Required Files**
Ensure these files exist in your repository:

**`requirements.txt`**:
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy>=2.0.25
psycopg2-binary>=2.9.9
alembic==1.12.1
pydantic>=2.5.0
psutil>=5.9.0
```

**`Procfile`**:
```
web: uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

**`runtime.txt`**:
```
python-3.11.9
```

**`nixpacks.toml`**:
```toml
[phases.setup]
aptPkgs = ["python3-pip", "python3.11-venv"]

[phases.build]
commands = ["pip install -r requirements.txt"]

[start]
cmd = "uvicorn src.main:app --host 0.0.0.0 --port $PORT"

[variables]
PYTHON_VERSION = "3.11"
```

### **Environment Variables**
Railway automatically configures:
- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - Application port (auto-assigned)

Manual configuration if needed:
```env
DATABASE_URL=postgresql://postgres:password@host:port/database
```

---

## 🗄️ **Database Setup**

### **Automatic Setup**
The application includes auto-setup on startup:
1. **Tables created** automatically
2. **Phone headings populated** on first run
3. **Health checks** available via API

### **Manual Database Setup**
If automatic setup fails:

**Via API**:
```bash
# Setup database tables and data
curl -X POST https://your-app.railway.app/admin/setup-database

# Check database status
curl https://your-app.railway.app/admin/database-status
```

**Via Railway Console**:
1. **PostgreSQL service** → **Database** tab
2. **Query** tab → Run SQL:
```sql
-- Create tables if needed
CREATE TABLE IF NOT EXISTS phone_headings (
    id SERIAL PRIMARY KEY,
    heading VARCHAR NOT NULL UNIQUE,
    region VARCHAR NOT NULL,
    status VARCHAR NOT NULL
);

-- Check data
SELECT COUNT(*) FROM phone_headings;
```

---

## 🌐 **Domain Configuration**

### **Generate Domain**
1. **Service** → **Networking** tab
2. **Generate Domain** button
3. **Port**: Leave empty or use any number (Railway overrides)
4. **Save** configuration

### **Custom Domain** (Optional)
1. **Custom Domain** button
2. **Add your domain**
3. **Configure DNS** as instructed
4. **SSL** automatically provisioned

---

## 🔍 **Monitoring & Debugging**

### **Application Logs**
1. **Service** → **Deployments** tab
2. **View Logs** for latest deployment
3. **Real-time monitoring** available

### **Database Monitoring**
1. **PostgreSQL service** → **Metrics** tab
2. **Connection count**, **Query performance**
3. **Storage usage** tracking

### **Health Checks**
```bash
# API Status
curl https://your-app.railway.app/

# Database Health
curl https://your-app.railway.app/health

# Admin Status
curl https://your-app.railway.app/admin/database-status
```

---

## 🚨 **Common Issues & Solutions**

### **Issue: Build Fails**
**Symptoms**: Deployment fails during build phase
**Solutions**:
1. Check `requirements.txt` format
2. Verify Python version in `runtime.txt`
3. Review build logs for specific errors

### **Issue: Database Connection Failed**
**Symptoms**: `localhost` connection errors
**Solutions**:
1. Verify `DATABASE_URL` environment variable
2. Check PostgreSQL service is running
3. Restart application service

### **Issue: Application Crashes**
**Symptoms**: Service shows "Crashed" status
**Solutions**:
1. Check startup logs for errors
2. Verify all dependencies installed
3. Test database connectivity

### **Issue: Domain Not Working**
**Symptoms**: URL returns connection errors
**Solutions**:
1. Verify domain generation completed
2. Check port configuration (should be empty)
3. Wait for DNS propagation (up to 24 hours)

---

## ⚡ **Performance Optimization**

### **Database Optimization**
```python
# Connection pooling (already configured)
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600
)
```

### **Application Optimization**
- **Async endpoints** for better concurrency
- **Response caching** for repeated queries
- **Connection reuse** for database operations

### **Railway Optimization**
- **Resource limits** configured automatically
- **Auto-scaling** based on traffic
- **CDN integration** for static assets

---

## 🔒 **Security Configuration**

### **Environment Security**
- **Database credentials** auto-generated
- **SSL/TLS** enabled by default
- **CORS** configured for web clients

### **API Security**
```python
# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Database Security**
- **Connection encryption** enabled
- **Access control** via Railway dashboard
- **Backup scheduling** available

---

## 📊 **Cost Management**

### **Free Tier Limits**
- **$5 monthly credit**
- **512MB RAM** per service
- **1GB storage** for PostgreSQL
- **100GB bandwidth**

### **Usage Monitoring**
1. **Project** → **Usage** tab
2. **Track resource consumption**
3. **Set up billing alerts**

### **Cost Optimization**
- **Sleep mode** for inactive services
- **Resource right-sizing**
- **Efficient database queries**

---

## 🔄 **Backup & Recovery**

### **Database Backups**
1. **PostgreSQL service** → **Backups** tab
2. **Manual backup** creation
3. **Automated backup** scheduling

### **Code Backups**
- **GitHub repository** as primary backup
- **Railway deployment history**
- **Local development environment**

### **Disaster Recovery**
1. **Redeploy from GitHub**
2. **Restore database from backup**
3. **Verify application functionality**

---

## 📈 **Scaling Strategy**

### **Vertical Scaling**
- **Upgrade Railway plan** for more resources
- **Increase database size** as needed
- **Monitor performance metrics**

### **Horizontal Scaling**
- **Multiple service instances**
- **Load balancer configuration**
- **Database read replicas**

---

## 🛠️ **Development Workflow**

### **Local to Production**
```bash
# Local development
uvicorn src.main:app --reload

# Test changes
python -m pytest

# Deploy to Railway
git push origin main
```

### **Environment Parity**
- **Same Python version** (3.11)
- **Identical dependencies**
- **Environment variable mapping**

### **CI/CD Pipeline**
- **Automatic deployment** on push
- **Build status notifications**
- **Rollback capabilities**

---

## 📞 **Support Resources**

### **Railway Documentation**
- [Railway Docs](https://docs.railway.app)
- [PostgreSQL Guide](https://docs.railway.app/databases/postgresql)
- [Python Deployment](https://docs.railway.app/languages/python)

### **Community Support**
- [Railway Discord](https://discord.gg/railway)
- [GitHub Issues](https://github.com/railwayapp/railway/issues)
- [Community Forum](https://help.railway.app)

### **Project Support**
- **Repository**: https://github.com/Hoangsonmoitapcode/fraud-detection-api
- **Issues**: GitHub Issues for bug reports
- **Documentation**: This guide and API docs

---

*Last Updated: September 2025*
*Railway Platform Version: Latest*
