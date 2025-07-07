@echo off
echo 🔧 Setting up Heroku CLI for Windows
echo ====================================
echo.

echo 🔍 Looking for Heroku installation...

REM Check common installation paths
set "HEROKU_PATHS=C:\Program Files\Heroku\bin;C:\Program Files (x86)\Heroku\bin;C:\Users\%USERNAME%\AppData\Local\Programs\Heroku\bin;C:\Users\%USERNAME%\AppData\Roaming\npm"

for %%p in (%HEROKU_PATHS%) do (
    if exist "%%p\heroku.exe" (
        echo ✅ Found Heroku at: %%p\heroku.exe
        echo.
        echo 🔧 Adding to PATH temporarily...
        set "PATH=%%p;%PATH%"
        echo.
        echo 🚀 Testing Heroku...
        heroku --version
        if %ERRORLEVEL% EQU 0 (
            echo.
            echo ✅ Heroku is working! Now let's deploy...
            echo.
            python deploy.py
            goto :end
        )
    )
)

echo ❌ Heroku CLI not found in common locations
echo.
echo 📥 Please try one of these solutions:
echo.
echo 1. Restart your computer after installing Heroku
echo 2. Install Heroku CLI via npm: npm install -g heroku
echo 3. Download from: https://devcenter.heroku.com/articles/heroku-cli
echo.
echo After installation, run this script again.

:end
echo.
echo Press any key to exit...
pause >nul 