@echo off
REM Windows batch script to clean up test screenshots
REM Usage: cleanup_screenshots.bat [--dry-run] [--execute] [--days N] [--max-files N]

echo Starting test screenshot cleanup...
echo.

REM Change to the project root directory
cd /d "%~dp0.."

REM Run the Python cleanup script with all arguments passed through
python scripts/cleanup_screenshots.py %*

echo.
echo Cleanup script completed.
pause 