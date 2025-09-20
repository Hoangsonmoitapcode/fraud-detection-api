@echo off
echo Database Management Tool
echo.

REM Change to project root directory
cd /d "%~dp0.."
echo Working directory: %cd%
echo.

echo Activating virtual environment...
call .venv\Scripts\activate
echo.

if "%1"=="" (
    echo Usage: manage_db.bat [command]
    echo.
    echo Available commands:
    echo   drop     - Drop all tables
    echo   create   - Create all tables
    echo   reset    - Drop and recreate tables ^(loses data!^)
    echo   migrate  - Apply pending migrations
    echo   status   - Show migration status
    echo   populate - Populate phone headings database
    echo.
    pause
    exit /b 1
)

echo Running: python scripts/manage_db.py %1
python scripts/manage_db.py %1
echo.
pause
