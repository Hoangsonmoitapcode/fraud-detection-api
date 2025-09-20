# 🌟 START HERE - New User Guide

**🎉 Welcome! You've received the Fraud Detection API project.**

This document will guide you through getting everything set up and running.

## 📁 **Quick Navigation**
- 🆕 **New to this project?** → Keep reading below
- 💻 **Experienced developer?** → See `README.md`
- 📋 **Want step-by-step?** → See `setup/SETUP_CHECKLIST.md`
- 📚 **Need detailed help?** → See `docs/INSTALLATION_GUIDE.md`
- 🗺️ **Lost in files?** → See `📁_DIRECTORY_GUIDE.md`

## 🎯 What This Project Does

This is a **Comprehensive Fraud Detection API** that:
- **📱 Phone Numbers**: Analyzes phone numbers for fraud risk with automatic region detection
- **💬 SMS Detection**: Detects spam/scam SMS messages with fuzzy matching
- **🏦 Banking Protection**: Identifies reported scam banking accounts
- **🌐 Website Safety**: Checks websites for phishing/scam content
- **📊 System Monitoring**: Real-time health checks and system metrics
- **🔧 Batch Processing**: Handle multiple items in single requests
- **📚 Interactive Docs**: Built-in API documentation and testing interface

## 📋 What You Need to Install First

**Don't have Python or PostgreSQL?** No problem! Follow these steps:

### 1. 🐍 Install Python (Required)
- Go to: https://python.org/downloads/
- Download **Python 3.11.x** (recommended) or 3.12.x
- **⚠️ IMPORTANT**: During installation, check "Add Python to PATH"

### 2. 🗄️ Install PostgreSQL (Required)  
- Go to: https://postgresql.org/download/windows/
- Download and install PostgreSQL
- **Remember the password** you set for the `postgres` user
- Use the default port `5432`

### 3. 📁 Set Up This Project
1. **Extract** the FraudDetection folder to your computer
2. **Open Command Prompt** in the project folder
3. **Run**: `setup\FIRST_TIME_SETUP.bat`

## 🚀 Quick Setup (3 Commands)

Once Python and PostgreSQL are installed:

```bash
# 1. Run the setup (installs everything)
setup\FIRST_TIME_SETUP.bat

# 2. Set up the database
database\manage_db.bat migrate

# 3. Start the server
scripts\start_server.bat
```

## 🌐 Access the Application

After starting the server, open your browser to:
- **🏠 API Status**: http://localhost:8000 ← **Check system health & available endpoints**
- **📚 Interactive Docs**: http://localhost:8000/docs ← **Start here to test APIs!**
- **🏥 Health Check**: http://localhost:8000/health ← **Monitor system health**
- **📖 ReDoc**: http://localhost:8000/redoc ← **Alternative documentation**

## 📚 Need More Help?

Choose your path:

### 🆕 **Complete Beginner**
→ Read: **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)**
→ Follow step-by-step checkboxes

### 📖 **Want Detailed Instructions**  
→ Read: **[docs/INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md)**
→ Complete installation guide with troubleshooting

### 💻 **Experienced Developer**
→ Read: **[README.md](README.md)**
→ Standard project documentation

## ⚡ Super Quick Test

Want to see if everything works?

1. **Start the server**: `scripts\start_server.bat`
2. **Check API Status**: http://localhost:8000 (should show system info & endpoints)
3. **Test Interactive Docs**: http://localhost:8000/docs
4. **Try the "Analyze" endpoint**:
   - Click on `POST /analyze/`
   - Click "Try it out"
   - Enter: `{"phone_numbers": ["0965842855"]}`
   - Click "Execute"
   - See the fraud risk analysis!
5. **Test other endpoints**: SMS, Banking, Website scam detection

## 🆘 Having Problems?

**Most common issues:**

1. **"Python is not recognized"**
   - Reinstall Python with "Add to PATH" checked

2. **"Database connection failed"**
   - Make sure PostgreSQL is running
   - Check your database password in `src\database.py`
   - Test with health check: http://localhost:8000/health

3. **"Port already in use"**
   - Close other applications using port 8000
   - Or restart your computer

4. **Setup script fails**
   - Make sure you have internet connection
   - Run Command Prompt as Administrator
   - Check if all dependencies are installed: `pip list`

5. **"Internal Server Error"**
   - Check if `psutil` is installed: `pip install psutil`
   - Restart the server: `scripts\start_server.bat`
   - Check logs for specific error messages

## 🎉 Success!

You'll know everything is working when:
- ✅ Server starts without errors
- ✅ API Status shows system healthy: http://localhost:8000
- ✅ Health check returns "healthy": http://localhost:8000/health
- ✅ Interactive docs load: http://localhost:8000/docs
- ✅ You can test all API endpoints (Phone, SMS, Banking, Website)
- ✅ System metrics display properly (CPU, Memory, Uptime)

---

**🚀 Ready to start? Run `FIRST_TIME_SETUP.bat` and follow the prompts!**
