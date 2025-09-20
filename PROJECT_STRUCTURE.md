# 📁 Project Structure Guide

## 🏗️ Organized Directory Structure

```
FraudDetection/
├── 🚀 START_HERE.md                    # ← Start here for new users
├── 📖 README.md                        # Main project documentation
├── 📋 CHANGELOG.md                     # Version history
│
├── 📂 setup/                           # 🛠️ SETUP & INSTALLATION
│   ├── FIRST_TIME_SETUP.bat           # Automated setup script
│   ├── SETUP_CHECKLIST.md             # Step-by-step checklist
│   └── quick-start.bat                 # Quick server start
│
├── 📂 config/                          # ⚙️ CONFIGURATION
│   ├── requirements.txt               # Python dependencies
│   └── env.example                    # Environment variables template
│
├── 📂 src/                             # 💻 APPLICATION CODE
│   ├── main.py                        # FastAPI app with all endpoints & monitoring
│   ├── database.py                    # Database configuration
│   ├── models.py                      # SQLAlchemy models (Phone, SMS, Banking, Website)
│   ├── schemas.py                     # Pydantic schemas for all endpoints
│   ├── phone_service.py               # Phone number analysis logic
│   └── populate_headings.py           # Phone headings data population
│
├── 📂 database/                        # 🗄️ DATABASE MANAGEMENT
│   ├── alembic/                       # Migration files
│   ├── alembic.ini                    # Migration config
│   ├── manage_db.py                   # Database management script
│   └── manage_db.bat                  # Database management wrapper
│
├── 📂 scripts/                         # 🔧 UTILITY SCRIPTS
│   ├── start_server.bat               # Start development server
│   └── setup.bat                      # Development setup
│
├── 📂 tests/                           # 🧪 TESTING
│   ├── __init__.py
│   ├── test_fraud_detection.py        # Phone number fraud detection tests
│   ├── test_new_scam_features.py      # SMS, Banking, Website tests
│   ├── test_unified_analyze_endpoint.py # Unified endpoint tests
│   ├── test_unified_batch_endpoints.py # Batch processing tests
│   └── test_unified_user_creation.py  # User creation tests
│
├── 🧪 test_api_status.py              # API status & health check testing
├── 🧪 test_with_json_data.py          # JSON data testing script
├── 📊 test_data_banking.json          # Banking test data
├── 📊 test_data_websites.json         # Website test data
│
├── 📂 docs/                            # 📚 DOCUMENTATION
│   ├── INSTALLATION_GUIDE.md          # Complete installation guide
│   ├── API.md                         # API documentation
│   ├── FRAUD_DETECTION_GUIDE.md       # User guide
│   ├── MIGRATION_GUIDE.md             # Database migration guide
│   └── TEST_RESULTS.md                # Test results
│
└── 📂 .venv/                          # 🐍 VIRTUAL ENVIRONMENT (auto-created)
    └── (Python packages)
```

## 🎯 Quick Navigation Guide

### 🆕 **New User? Start Here:**
```
1. 📖 START_HERE.md              # Overview and quick start
2. 📂 setup/FIRST_TIME_SETUP.bat # Run this first
3. 📋 setup/SETUP_CHECKLIST.md   # Follow the checklist
```

### 💻 **Developer? Go Here:**
```
1. 📖 README.md                  # Full documentation
2. 📂 src/                       # Application code
3. 📂 tests/                     # Test files
4. 📚 docs/API.md               # API documentation
```

### 🔧 **Need to Configure?**
```
1. 📂 config/requirements.txt    # Add/remove packages
2. 📂 src/database.py           # Database settings
3. 📂 config/env.example        # Environment variables
```

### 🗄️ **Database Issues?**
```
1. 📂 database/manage_db.bat    # Database commands
2. 📂 database/alembic/         # Migration files
3. 📚 docs/MIGRATION_GUIDE.md   # Migration help
```

## 🚀 Common Tasks & File Locations

| Task | File/Command | Location |
|------|-------------|----------|
| **First Setup** | `FIRST_TIME_SETUP.bat` | `setup/` |
| **Start Server** | `start_server.bat` | `scripts/` |
| **Quick Start** | `quick-start.bat` | `setup/` |
| **Database Setup** | `manage_db.bat migrate` | `database/` |
| **Add Dependencies** | Edit `requirements.txt` | `config/` |
| **Change DB Config** | Edit `database.py` | `src/` |
| **Check API Status** | Visit `/` | http://localhost:8000 |
| **View API Docs** | Visit `/docs` | http://localhost:8000/docs |
| **Health Check** | Visit `/health` | http://localhost:8000/health |
| **Test API Status** | `python test_api_status.py` | Root directory |
| **Test with JSON** | `python test_with_json_data.py` | Root directory |
| **Run All Tests** | Files in `tests/` folder | `tests/` |

## 📋 File Categories

### 🔵 **Essential Files (Don't Delete)**
- `src/main.py` - Main FastAPI app with all endpoints & monitoring
- `src/database.py` - Database connection and configuration
- `src/models.py` - SQLAlchemy models (User, SMS, Banking, Website)
- `src/schemas.py` - Pydantic schemas for all API endpoints
- `src/phone_service.py` - Phone number analysis business logic
- `config/requirements.txt` - Python dependencies (including psutil)
- `database/alembic/` - Database migrations

### 🟢 **Setup Files (For New Users)**
- `START_HERE.md` - Entry point
- `setup/FIRST_TIME_SETUP.bat` - Automated setup
- `setup/SETUP_CHECKLIST.md` - Manual checklist
- `docs/INSTALLATION_GUIDE.md` - Detailed guide

### 🟡 **Development Files**
- `scripts/start_server.bat` - Development server startup
- `test_api_status.py` - API status & health testing script
- `test_with_json_data.py` - JSON data testing script
- `tests/` - Comprehensive test suite (Phone, SMS, Banking, Website)
- `docs/API.md` - API documentation
- `CHANGELOG.md` - Version history with v3.1.0 updates

### 🟠 **Configuration Files**
- `config/env.example` - Environment template
- `database/alembic.ini` - Migration config
- `.gitignore` - Git exclusions

## 🎨 Visual File Icons Legend

- 🚀 **Start/Launch files** - Entry points and startup scripts
- 📖 **Documentation** - README, guides, help files
- 📂 **Directories** - Organized folders
- 💻 **Code files** - Python application code
- 🗄️ **Database files** - Migration and DB management
- 🔧 **Utility scripts** - Helper and setup scripts
- ⚙️ **Configuration** - Settings and config files
- 🧪 **Testing** - Test files and results
- 📚 **Documentation** - Detailed guides and docs

## 🎯 Benefits of This Structure

✅ **Clear Separation** - Each type of file has its place
✅ **Easy Navigation** - Logical grouping by function
✅ **New User Friendly** - Setup files are prominent
✅ **Developer Friendly** - Code and docs are organized
✅ **Scalable** - Easy to add new features
✅ **Professional** - Industry-standard organization
