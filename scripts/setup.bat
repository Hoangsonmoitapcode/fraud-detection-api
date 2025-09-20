@echo off
echo Setting up Fraud Detection API...
echo.

REM Change to project root directory
cd /d "%~dp0.."
echo Working directory: %cd%
echo.

echo Creating virtual environment...
python -m venv .venv
echo.

echo Activating virtual environment...
call .venv\Scripts\activate
echo.

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
echo.

echo Setup complete!
echo.
echo Next steps:
echo 1. Configure your database in src/database.py
echo 2. Run database migrations: python scripts/manage_db.py
echo 3. Start the server: scripts/start_server.bat
echo.
pause
