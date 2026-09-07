@echo off
title TenderRadar - FIX and RUN
cd /d "%~dp0"

echo.
echo ============================================
echo   TenderRadar - get latest code and run
echo ============================================
echo.
echo Folder: %CD%
echo.

where git >nul 2>&1
if errorlevel 1 (
  echo ERROR: git not installed. Install Git for Windows first.
  pause
  exit /b 1
)

echo [1] Pulling latest from GitHub...
git fetch origin main
git reset --hard origin/main
if errorlevel 1 (
  echo.
  echo FAILED. If this is not a git folder, clone fresh:
  echo   cd C:\Users\Admin\Desktop
  echo   git clone https://github.com/Kamo2330/TenderRadar.git
  pause
  exit /b 1
)

echo.
echo [2] Installing packages...
pip install -r requirements.txt

echo.
echo [3] Database and sample tenders...
python manage.py migrate
python manage.py load_sample_tenders

echo.
echo [4] Starting server...
echo.
echo CHECK THIS FIRST in browser:
echo   http://127.0.0.1:8000/health/
echo.
echo Must say:  UI: table-v3
echo.
echo Then open (use Incognito or Ctrl+F5):
echo   http://127.0.0.1:8000/
echo.
echo Footer must say: Interface table-v3
echo ============================================

python manage.py runserver
