@echo off
echo 🚀 Transport Admin Portal - Cloud Deployment
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "app.py" (
    echo ❌ Please run this script from the transport application directory
    echo Expected: python/plugins/transPort/
    pause
    exit /b 1
)

REM Run the deployment script
echo 🔄 Starting deployment...
python deploy.py

echo.
echo Press any key to exit...
pause >nul 