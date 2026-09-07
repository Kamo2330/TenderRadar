@echo off
title Update TenderRadar
cd /d "%~dp0"

echo.
echo ============================================
echo   Updating TenderRadar from GitHub
echo ============================================
echo.

git pull origin main
if errorlevel 1 (
  echo.
  echo GIT PULL FAILED. Check your internet or folder path.
  pause
  exit /b 1
)

pip install -r requirements.txt
python manage.py migrate
python manage.py load_sample_tenders

echo.
echo ============================================
echo   Update complete
echo ============================================
echo.
echo 1. STOP the old server  ^(Ctrl+C in its window^)
echo 2. Start again:  python manage.py runserver
echo 3. Open:  http://127.0.0.1:8000/health/
echo    Must show:  UI: table-v3
echo 4. Open site in INCOGNITO or press Ctrl+F5
echo.
pause
