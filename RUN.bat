@echo off
title TenderRadar on port 8001
cd /d "%~dp0"

echo.
echo ============================================
echo   TenderRadar - port 8001
echo   (Qasha often uses port 8000 - avoid it)
echo ============================================
echo.

echo [1] Free ports 8000 and 8001...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /PID %%a /F >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8001 ^| findstr LISTENING') do taskkill /PID %%a /F >nul 2>&1

echo [2] Install packages (optional API fix)...
pip install "django>=6.0,<6.1" "djangorestframework>=3.18,<4" -r requirements.txt
echo.

if not exist .env copy .env.example .env >nul
python manage.py migrate --fake-initial >nul 2>&1
python manage.py migrate >nul 2>&1

echo [3] Starting server...
echo.
echo OPEN IN INCOGNITO:
echo   http://127.0.0.1:8001/health/
echo.
echo Must show: TENDERRADAR OK
echo Then open: http://127.0.0.1:8001/
echo.
echo ============================================

python manage.py runserver 8001
