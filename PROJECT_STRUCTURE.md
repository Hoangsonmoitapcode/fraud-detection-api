# 📁 Project Structure

## 🏗️ **Directory Organization**

```
fraud-detection-api/
├── 📄 README.md                          # Main project documentation
├── 📄 COMPREHENSIVE_README.md            # Detailed technical guide
├── 📄 PROJECT_STRUCTURE.md               # This file
├── 📄 CHANGELOG.md                       # Version history
├── 📄 START_HERE.md                      # Quick start guide
├── 📄 LICENSE                            # MIT License
├── 📄 .gitignore                         # Git ignore rules
│
├── 🚀 **Deployment Configuration**
│   ├── 📄 requirements.txt               # Python dependencies
│   ├── 📄 Procfile                       # Railway deployment config
│   ├── 📄 runtime.txt                    # Python version specification
│   └── 📄 nixpacks.toml                  # Railway build configuration
│
├── 📚 **documentation/**                 # Organized documentation
│   ├── 📁 guides/                        # User and developer guides
│   │   ├── 📄 API.md                     # API reference
│   │   ├── 📄 FRAUD_DETECTION_GUIDE.md  # Fraud detection methodology
│   │   ├── 📄 INSTALLATION_GUIDE.md     # Local installation
│   │   ├── 📄 MIGRATION_GUIDE.md        # Database migrations
│   │   └── 📄 TEST_RESULTS.md           # Testing documentation
│   ├── 📁 examples/                      # Code examples and testing
│   │   └── 📄 test_railway_database.py  # Railway testing script
│   └── 📁 deployment/                    # Deployment guides
│       └── 📄 RAILWAY_COMPLETE_GUIDE.md # Complete Railway setup
│
├── 🗄️ **database/**                      # Database management
│   ├── 📄 manage_db.py                   # Database management script
│   ├── 📄 manage_db.bat                  # Windows batch script
│   ├── 📄 alembic.ini                    # Alembic configuration
│   └── 📁 alembic/                       # Database migrations
│       ├── 📄 env.py                     # Migration environment
│       ├── 📄 script.py.mako             # Migration template
│       └── 📁 versions/                  # Migration versions
│
├── 💻 **src/**                           # Source code
│   ├── 📄 __init__.py                    # Package initialization
│   ├── 📄 main.py                        # FastAPI application
│   ├── 📄 database.py                    # Database configuration
│   ├── 📄 models.py                      # SQLAlchemy models
│   ├── 📄 schemas.py                     # Pydantic schemas
│   ├── 📄 phone_service.py               # Phone analysis logic
│   └── 📄 populate_headings.py           # Database population
│
├── 🧪 **tests/**                         # Test suite
│   ├── 📄 __init__.py                    # Test package initialization
│   ├── 📄 test_fraud_detection.py        # Core functionality tests
│   ├── 📄 test_batch_phone_analysis.py   # Batch processing tests
│   ├── 📄 test_batch_user_create.py      # User creation tests
│   ├── 📄 test_new_scam_features.py      # New feature tests
│   ├── 📄 test_unified_analyze_endpoint.py # Analysis endpoint tests
│   ├── 📄 test_unified_batch_endpoints.py # Batch endpoint tests
│   └── 📄 test_unified_user_creation.py  # Unified user tests
│
├── 🛠️ **scripts/**                       # Utility scripts
│   ├── 📄 setup.bat                      # Windows setup script
│   └── 📄 start_server.bat               # Server start script
│
├── ⚙️ **setup/**                         # Setup and configuration
│   ├── 📄 FIRST_TIME_SETUP.bat          # First-time setup
│   ├── 📄 quick-start.bat               # Quick start script
│   └── 📄 SETUP_CHECKLIST.md            # Setup checklist
│
└── 📊 **Test Data**                      # Sample data for testing
    ├── 📄 test_data_banking.json         # Banking test data
    ├── 📄 test_data_websites.json        # Website test data
    └── 📄 test_with_json_data.py          # JSON data testing
```

---

## 🔧 **Core Components**

### **Application Core (`src/`)**

#### **`main.py`** - FastAPI Application
- **FastAPI app initialization**
- **API endpoint definitions**
- **Middleware configuration**
- **Auto-startup database population**
- **Admin endpoints for Railway**

#### **`database.py`** - Database Configuration
- **SQLAlchemy engine setup**
- **Connection pooling**
- **Environment variable handling**
- **Connection testing utilities**

#### **`models.py`** - Database Models
- **SQLAlchemy ORM models**
- **Table relationships**
- **Database schema definitions**

#### **`schemas.py`** - API Schemas
- **Pydantic models for API**
- **Request/response validation**
- **Data serialization**

#### **`phone_service.py`** - Phone Analysis Logic
- **Phone number parsing**
- **Regional detection**
- **Fraud risk assessment**
- **Vietnamese carrier database**
- **Landline regional mapping**

#### **`populate_headings.py`** - Data Population
- **Initial data seeding**
- **Phone heading database**
- **International number mapping**

---

## 📚 **Documentation Structure**

### **Main Documentation**
- **`README.md`**: Project overview and quick start
- **`COMPREHENSIVE_README.md`**: Complete technical documentation
- **`START_HERE.md`**: New user onboarding guide
- **`PROJECT_STRUCTURE.md`**: This file - project organization

### **Guides (`documentation/guides/`)**
- **`API.md`**: Complete API reference
- **`FRAUD_DETECTION_GUIDE.md`**: Fraud detection methodology
- **`INSTALLATION_GUIDE.md`**: Local development setup
- **`MIGRATION_GUIDE.md`**: Database migration procedures
- **`TEST_RESULTS.md`**: Testing documentation and results

### **Examples (`documentation/examples/`)**
- **`test_railway_database.py`**: Railway deployment testing
- **Sample API calls and responses**
- **Integration examples**

### **Deployment (`documentation/deployment/`)**
- **`RAILWAY_COMPLETE_GUIDE.md`**: Complete Railway deployment guide
- **Environment configuration**
- **Production deployment procedures**

---

## 🗄️ **Database Management**

### **Migration System (`database/alembic/`)**
```
alembic/
├── 📄 env.py                    # Migration environment
├── 📄 script.py.mako            # Migration template
└── 📁 versions/                 # Version history
    ├── 📄 c7f62bf6c2f1_initial_migration.py
    ├── 📄 2cbf396a1b06_add_created_at_column.py
    ├── 📄 36eb31201950_add_sms_banking_and_website_scam_tables.py
    └── 📄 ffaca50b7a1e_add_phone_headings_table_and_user_.py
```

### **Management Scripts**
- **`manage_db.py`**: Cross-platform database management
- **`manage_db.bat`**: Windows-specific batch script
- **`alembic.ini`**: Alembic configuration

---

## 🧪 **Testing Structure**

### **Test Categories**
- **Core functionality**: Basic fraud detection
- **Batch processing**: Multiple item analysis
- **User management**: User creation and management
- **API endpoints**: Endpoint-specific testing
- **Integration**: End-to-end testing

### **Test Data**
- **`test_data_banking.json`**: Banking scam examples
- **`test_data_websites.json`**: Website scam examples
- **`test_with_json_data.py`**: JSON-based testing

---

## 🚀 **Deployment Configuration**

### **Railway Platform**
- **`Procfile`**: Process definition
- **`runtime.txt`**: Python version
- **`nixpacks.toml`**: Build configuration
- **`requirements.txt`**: Dependencies

### **Environment Variables**
```env
DATABASE_URL=postgresql://...    # Auto-configured by Railway
PORT=8000                       # Auto-assigned by Railway
```

---

## 📊 **Data Flow**

### **Request Processing**
```
Client Request → FastAPI → Phone Service → Database → Response
                    ↓
              Validation (Pydantic)
                    ↓
              Business Logic
                    ↓
              Database Query (SQLAlchemy)
                    ↓
              Response Formatting
```

### **Database Schema**
```sql
phone_headings (id, heading, region, status)
users (id, phone_number, phone_head, phone_region, label, heading_id)
sms_scams (id, message, risk_level, detected_patterns, analysis_result)
banking_scams (id, message, risk_level, detected_patterns, analysis_result)
website_scams (id, url, risk_level, detected_patterns, analysis_result)
```

---

## 🔧 **Development Workflow**

### **Local Development**
1. **Clone repository**
2. **Setup virtual environment**
3. **Install dependencies**
4. **Configure database**
5. **Run migrations**
6. **Start development server**

### **Production Deployment**
1. **Push to GitHub**
2. **Railway auto-deployment**
3. **Database auto-configuration**
4. **Health check verification**

---

## 📈 **File Size & Complexity**

### **Core Files (by importance)**
1. **`src/main.py`** (689 lines) - Main application
2. **`src/phone_service.py`** (177 lines) - Phone analysis logic
3. **`COMPREHENSIVE_README.md`** - Complete documentation
4. **`documentation/deployment/RAILWAY_COMPLETE_GUIDE.md`** - Deployment guide

### **Configuration Files**
- **`requirements.txt`** (8 lines) - Dependencies
- **`Procfile`** (2 lines) - Process definition
- **`runtime.txt`** (2 lines) - Python version
- **`nixpacks.toml`** (11 lines) - Build config

---

## 🎯 **Navigation Tips**

### **For New Users**
1. **Start**: `README.md`
2. **Setup**: `START_HERE.md`
3. **Quick Start**: `setup/quick-start.bat`

### **For Developers**
1. **Code**: `src/` directory
2. **Tests**: `tests/` directory
3. **API Docs**: `documentation/guides/API.md`

### **For Deployment**
1. **Railway Guide**: `documentation/deployment/RAILWAY_COMPLETE_GUIDE.md`
2. **Configuration**: Root-level config files
3. **Database**: `database/` directory

---

*Last Updated: September 2025*
*Total Files: 50+ files across 10 directories*
