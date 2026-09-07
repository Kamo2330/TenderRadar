@echo off
title TenderRadar on port 8765
cd /d "%~dp0"

echo.
echo ============================================
echo   TenderRadar - port 8765
echo ============================================
echo.

echo [1] Free port 8765...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8765 ^| findstr LISTENING') do taskkill /PID %%a /F >nul 2>&1

echo [2] Install packages...
pip install -r requirements.txt
echo.

if not exist .env copy .env.example .env >nul
python manage.py migrate --fake-initial >nul 2>&1
python manage.py migrate >nul 2>&1

echo [3] Starting server...
echo.
echo Open: http://127.0.0.1:8765/
echo Health check: http://127.0.0.1:8765/health/
echo Run VERIFY.bat in another window to test without browser.
echo ============================================

python manage.py runserver 8765
