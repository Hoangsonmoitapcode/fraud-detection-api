# 📋 Setup Checklist for New Users

Use this checklist to ensure everything is properly installed and configured.

## ✅ Pre-Installation Checklist

### Step 1: Install Python
- [ ] Download Python 3.11.x from https://python.org/downloads/
- [ ] During installation, **CHECK "Add Python to PATH"**
- [ ] Complete Python installation
- [ ] Open Command Prompt and verify: `python --version`
- [ ] Verify pip works: `pip --version`

### Step 2: Install PostgreSQL
- [ ] Download PostgreSQL from https://postgresql.org/download/windows/
- [ ] Install PostgreSQL (remember the postgres password!)
- [ ] Keep default port 5432
- [ ] Verify installation: `psql --version`

### Step 3: Set Up Database
- [ ] Open pgAdmin (comes with PostgreSQL)
- [ ] Connect to PostgreSQL server (localhost:5432)
- [ ] Create new database named: `fastapi_db`
- [ ] Note down your database credentials

## 🚀 Project Setup Checklist

### Step 4: Extract and Configure Project
- [ ] Extract FraudDetection folder to desired location
- [ ] Open `src\database.py` in text editor
- [ ] Update DATABASE_URL with your PostgreSQL credentials:
  ```
  postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/fastapi_db
  ```

### Step 5: Run Setup
- [ ] Open Command Prompt in project folder
- [ ] Run: `FIRST_TIME_SETUP.bat`
- [ ] Wait for all dependencies to install
- [ ] Look for "Setup Complete!" message

### Step 6: Initialize Database
- [ ] Run: `scripts\manage_db.bat migrate`
- [ ] (Optional) Run: `scripts\manage_db.bat populate`
- [ ] Verify no error messages appear

### Step 7: Start Server
- [ ] Run: `scripts\start_server.bat`
- [ ] Look for "Application startup complete" message
- [ ] Open browser to: http://localhost:8000/docs
- [ ] Verify API documentation page loads

## 🎯 Success Verification

You should be able to:
- [ ] See Python version when typing `python --version`
- [ ] Connect to PostgreSQL with pgAdmin
- [ ] Run setup script without errors
- [ ] Start server successfully
- [ ] Access API documentation at http://localhost:8000/docs
- [ ] Test API endpoints in the documentation

## 🆘 Common Issues & Solutions

### "Python is not recognized"
- Reinstall Python with "Add to PATH" checked
- Restart Command Prompt after installation

### "Connection to database failed"
- Check PostgreSQL service is running (Windows Services)
- Verify database name and credentials in `src\database.py`
- Make sure database `fastapi_db` exists

### "Port 8000 already in use"
- Close any other applications using port 8000
- Or edit startup script to use different port

### "Module not found" errors
- Make sure virtual environment is activated
- Re-run: `pip install -r requirements.txt`

## 📞 Need Help?

If you encounter issues:
1. Check the detailed guide: `docs\INSTALLATION_GUIDE.md`
2. Look at error messages in the terminal
3. Verify all checkboxes above are completed
4. Contact the project maintainer with specific error messages

---

**🎉 Once all items are checked, your Fraud Detection API is ready to use!**
