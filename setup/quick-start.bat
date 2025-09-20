@echo off
echo ========================================
echo   Fraud Detection API - Quick Start
echo ========================================
echo.

echo Activating virtual environment...
call .venv\Scripts\activate
echo.

echo Starting the server...
echo.
echo Server URLs:
echo   - API: http://localhost:8000
echo   - Docs: http://localhost:8000/docs
echo   - ReDoc: http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
