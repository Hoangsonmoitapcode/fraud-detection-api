# 📁 Visual Directory Guide

## 🎯 **Quick Access Menu**

| What do you want to do? | Go to this file |
|-------------------------|-----------------|
| 🆕 **First time setup** | `setup/FIRST_TIME_SETUP.bat` |
| 🚀 **Start the server** | `scripts/start_server.bat` |
| 📖 **Read documentation** | `README.md` |
| 🔧 **Manage database** | `database/manage_db.bat` |
| 🧪 **Run tests** | `tests/test_fraud_detection.py` |
| 📚 **API documentation** | `docs/API.md` |

---

## 📂 **Current Directory Structure**

```
📁 FraudDetection/
│
├── 🚀 START_HERE.md                     ← 🌟 NEW USERS START HERE
├── 📖 README.md                         ← 📚 Main documentation
├── 📋 CHANGELOG.md                      ← 📝 Version history
├── 📁 PROJECT_STRUCTURE.md             ← 🗺️ This guide
│
├── 📂 setup/                            ← 🛠️ SETUP & FIRST TIME USERS
│   ├── 🔧 FIRST_TIME_SETUP.bat         ← 🌟 Run this first!
│   ├── 📋 SETUP_CHECKLIST.md           ← ✅ Step-by-step guide
│   └── ⚡ quick-start.bat              ← 🚀 Quick server start
│
├── 📂 config/                           ← ⚙️ CONFIGURATION FILES
│   ├── 📦 requirements.txt             ← 🐍 Python packages
│   └── 🔐 env.example                  ← 🌍 Environment template
│
├── 📂 src/                              ← 💻 APPLICATION CODE
│   ├── 🎯 main.py                      ← 🌟 Main FastAPI app
│   ├── 🗄️ database.py                 ← 🔗 Database connection
│   ├── 📊 models.py                    ← 🏗️ Data models
│   ├── 📋 schemas.py                   ← 📝 API schemas
│   ├── 📞 phone_service.py             ← 🧠 Business logic
│   └── 📥 populate_headings.py         ← 📊 Data seeding
│
├── 📂 database/                         ← 🗄️ DATABASE MANAGEMENT
│   ├── 📂 alembic/                     ← 🔄 Migration files
│   ├── ⚙️ alembic.ini                  ← 🔧 Migration config
│   ├── 🐍 manage_db.py                 ← 🛠️ DB management script
│   └── 🔧 manage_db.bat                ← 🎯 DB commands (Windows)
│
├── 📂 scripts/                          ← 🔧 UTILITY SCRIPTS
│   ├── 🚀 start_server.bat             ← 🌟 Start development server
│   └── 🛠️ setup.bat                   ← 🔧 Development setup
│
├── 📂 tests/                            ← 🧪 TESTING
│   ├── 📄 __init__.py                  ← 🐍 Python package
│   └── 🧪 test_fraud_detection.py      ← ✅ Test suite
│
├── 📂 docs/                             ← 📚 DOCUMENTATION
│   ├── 📖 INSTALLATION_GUIDE.md        ← 🛠️ Complete install guide
│   ├── 📡 API.md                       ← 🔌 API documentation
│   ├── 🛡️ FRAUD_DETECTION_GUIDE.md    ← 👤 User guide
│   ├── 🔄 MIGRATION_GUIDE.md           ← 🗄️ Database migrations
│   └── 📊 TEST_RESULTS.md              ← 🧪 Test results
│
└── 📂 .venv/                            ← 🐍 VIRTUAL ENVIRONMENT
    └── (auto-created Python packages)
```

---

## 🎨 **File Type Legend**

| Icon | Type | Description |
|------|------|-------------|
| 🌟 | **Essential** | Must-use files for key functions |
| 🚀 | **Startup** | Files that launch or start things |
| 📖 | **Documentation** | README files and guides |
| 🔧 | **Scripts** | Executable batch/Python files |
| 📂 | **Directories** | Folders containing related files |
| 💻 | **Code** | Python application code |
| 🗄️ | **Database** | Database-related files |
| ⚙️ | **Config** | Configuration files |
| 🧪 | **Testing** | Test files and results |
| 📚 | **Docs** | Detailed documentation |

---

## 🎯 **Usage Workflows**

### 🆕 **New User Workflow**
```
1. 📖 Read START_HERE.md
2. 🔧 Run setup/FIRST_TIME_SETUP.bat
3. 📋 Follow setup/SETUP_CHECKLIST.md
4. 🚀 Run scripts/start_server.bat
5. 🌐 Visit http://localhost:8000/docs
```

### 💻 **Developer Workflow**
```
1. 📖 Read README.md
2. 💻 Explore src/ directory
3. 🧪 Run tests/ files
4. 📚 Check docs/API.md
5. 🔧 Use scripts/ for development
```

### 🔧 **Maintenance Workflow**
```
1. 🗄️ Use database/manage_db.bat for DB tasks
2. ⚙️ Edit config/ files for settings
3. 📊 Update src/ for new features
4. 🧪 Add tests/ for new code
5. 📚 Update docs/ for changes
```

---

## 🎪 **Visual Navigation Tips**

- 🌟 **Gold stars** = Most important files
- 🚀 **Rockets** = Files that start/launch things
- 📂 **Folders** = Organized by function
- 🎯 **Targets** = Entry points and main files

**Everything is organized by PURPOSE, not just file type!** 🎯
