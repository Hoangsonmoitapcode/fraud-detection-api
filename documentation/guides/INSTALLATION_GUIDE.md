# 🚀 Complete Installation Guide

This guide will help you set up the Fraud Detection API from scratch, even if you don't have Python or PostgreSQL installed.

## 📋 Prerequisites

Your friend will need to install:
1. **Python 3.11+** 
2. **PostgreSQL Database**
3. **Git** (optional, for version control)

---

## 🐍 Step 1: Install Python

### Option A: From Python.org (Recommended)
1. **Download Python**:
   - Go to https://www.python.org/downloads/
   - Download Python 3.11.x or 3.12.x (avoid 3.13 for better compatibility)
   - Choose the "Windows installer (64-bit)"

2. **Install Python**:
   - Run the downloaded installer
   - ⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation**:
   ```bash
   python --version
   pip --version
   ```

### Option B: From Microsoft Store (Alternative)
1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Install the official Python package

---

## 🗄️ Step 2: Install PostgreSQL

### Download and Install
1. **Download PostgreSQL**:
   - Go to https://www.postgresql.org/download/windows/
   - Download the latest version (15.x or 16.x)
   - Choose the Windows installer

2. **Install PostgreSQL**:
   - Run the installer
   - **Remember the password** you set for the `postgres` user
   - Use default port `5432`
   - Complete the installation

3. **Verify Installation**:
   - Open Command Prompt or PowerShell
   - Type: `psql --version`

### Create Database
1. **Open pgAdmin** (installed with PostgreSQL)
2. **Connect to PostgreSQL**:
   - Server: localhost
   - Port: 5432
   - Username: postgres
   - Password: (the one you set during installation)

3. **Create Database**:
   - Right-click "Databases" → "Create" → "Database"
   - Database name: `fastapi_db`
   - Owner: postgres
   - Click "Save"

4. **Create User** (Optional but recommended):
   - Right-click "Login/Group Roles" → "Create" → "Login/Group Role"
   - Name: `fastapi_user`
   - Password: `mypassword` (or choose your own)
   - Privileges: Check "Can login?" and "Superuser?"
   - Click "Save"

---

## 📁 Step 3: Set Up the Project

### 1. Extract Project Files
- Extract the FraudDetection folder to your desired location
- Example: `C:\Projects\FraudDetection`

### 2. Update Database Configuration
1. **Open** `src\database.py`
2. **Update the DATABASE_URL** if needed:
   ```python
   # If you used default postgres user:
   DATABASE_URL = "postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/fastapi_db"
   
   # If you created fastapi_user:
   DATABASE_URL = "postgresql+psycopg2://fastapi_user:mypassword@localhost:5432/fastapi_db"
   ```

### 3. Run Setup Script
1. **Open Command Prompt or PowerShell**
2. **Navigate to project folder**:
   ```bash
   cd C:\Projects\FraudDetection
   ```
3. **Run setup**:
   ```bash
   scripts\setup.bat
   ```

This will:
- Create virtual environment
- Install all Python dependencies
- Set up the project

---

## 🚀 Step 4: Start the Application

### 1. Set Up Database Tables
```bash
scripts\manage_db.bat migrate
```

### 2. Populate Initial Data (Optional)
```bash
scripts\manage_db.bat populate
```

### 3. Start the Server
```bash
scripts\start_server.bat
```

Or use the quick start:
```bash
quick-start.bat
```

### 4. Test the Application
- Open browser and go to: http://localhost:8000/docs
- You should see the API documentation

---

## 🔧 Troubleshooting

### Python Issues
**Problem**: "Python is not recognized"
**Solution**: 
1. Reinstall Python with "Add to PATH" checked
2. Or manually add Python to PATH:
   - Search "Environment Variables" in Windows
   - Add Python installation folder to PATH

**Problem**: "pip is not recognized"
**Solution**: Same as above, ensure Scripts folder is in PATH

### PostgreSQL Issues
**Problem**: "Connection refused"
**Solution**:
1. Check if PostgreSQL service is running:
   - Windows Services → PostgreSQL service → Start
2. Verify database exists and credentials are correct

**Problem**: "psycopg2 installation failed"
**Solution**:
1. Install Microsoft Visual C++ Build Tools
2. Or use: `pip install psycopg2-binary` (already in requirements.txt)

### Port Issues
**Problem**: "Port 8000 already in use"
**Solution**:
1. Kill any running Python processes
2. Or change port in startup script:
   ```bash
   python -m uvicorn src.main:app --reload --port 8001
   ```

---

## 📖 Quick Reference Commands

```bash
# Setup (run once)
scripts\setup.bat

# Database management
scripts\manage_db.bat migrate    # Apply migrations
scripts\manage_db.bat populate   # Add initial data
scripts\manage_db.bat status     # Check migration status

# Start server
scripts\start_server.bat         # Full startup
quick-start.bat                  # Quick start

# Stop server
# Press Ctrl+C in the terminal
```

---

## 🆘 Getting Help

If your friend encounters issues:

1. **Check the logs** in the terminal for error messages
2. **Verify installations**:
   ```bash
   python --version
   pip --version
   psql --version
   ```
3. **Check database connection**:
   ```bash
   scripts\manage_db.bat status
   ```
4. **Try the test endpoints** at http://localhost:8000/docs

---

## 🎯 Success Checklist

Your friend should be able to:
- ✅ See "Python 3.x.x" when running `python --version`
- ✅ Connect to PostgreSQL with pgAdmin
- ✅ Run `scripts\setup.bat` without errors
- ✅ Start the server with `scripts\start_server.bat`
- ✅ Access http://localhost:8000/docs in browser
- ✅ See the API documentation and test endpoints

---

## 💡 Tips for Your Friend

1. **Use Windows PowerShell** or Command Prompt as Administrator if you encounter permission issues
2. **Keep the terminal open** while the server is running
3. **Use the API documentation** at `/docs` to test the endpoints
4. **Check the logs** in the terminal if something doesn't work
5. **Restart the server** after making code changes (unless using `--reload`)

---

## 🔄 Alternative: Docker Setup (Advanced)

For a more isolated setup, you could also provide a Docker configuration, but the above method is simpler for beginners.
