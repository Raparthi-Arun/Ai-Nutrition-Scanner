@echo off
REM NutriScan Backend Quick Setup Script for Windows

echo.
echo ========================================
echo   NutriScan Backend Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    exit /b 1
)

echo [1/5] Navigating to backend directory...
cd backend
if errorlevel 1 (
    echo ERROR: Could not find backend directory
    exit /b 1
)

echo [2/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    exit /b 1
)

echo [3/5] Activating virtual environment and installing dependencies...
call venv\Scripts\Activate.ps1
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)

echo [4/5] Running database migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to run migrations
    exit /b 1
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Create a superuser (admin account):
echo    python manage.py createsuperuser
echo.
echo 2. Start the development server:
echo    python manage.py runserver 0.0.0.0:8000
echo.
echo Then open your frontend in another terminal:
echo    - Open index.html in VS Code with Live Server
echo    - Or visit: http://localhost:5500/
echo.
echo Backend will be available at:
echo    http://localhost:8000/api/
echo.
echo Admin panel:
echo    http://localhost:8000/admin/
echo.
echo For more information, see:
echo    - backend/README.md
echo    - SETUP.md
echo    - INTEGRATION_SUMMARY.md
echo.
pause
