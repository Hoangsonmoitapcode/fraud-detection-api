@echo off
echo ========================================
echo   Fraud Detection API - First Time Setup
echo ========================================
echo.
echo This script will help you set up the Fraud Detection API.
echo Make sure you have installed:
echo   - Python 3.11+ (with "Add to PATH" checked)
echo   - PostgreSQL database
echo.
pause

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

python --version
echo ✅ Python is installed
echo.

echo Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo ✅ pip is available
echo.

echo Creating virtual environment...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment created
echo.

echo Activating virtual environment...
call .venv\Scripts\activate

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    echo Check your internet connection and try again
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure PostgreSQL is running
echo 2. Create database 'fastapi_db' in PostgreSQL
echo 3. Update database credentials in src\database.py if needed
echo 4. Run: scripts\manage_db.bat migrate
echo 5. Run: scripts\start_server.bat
echo.
echo For detailed instructions, see: docs\INSTALLATION_GUIDE.md
echo.
pause
