@echo off
echo Starting Fraud Detection API Server...
echo.

REM Change to project root directory
cd /d "%~dp0.."
echo Working directory: %cd%
echo.

echo Activating virtual environment...
call .venv\Scripts\activate
echo.
echo Starting FastAPI server...
echo Server will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
pause