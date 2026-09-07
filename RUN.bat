@echo off
title TenderRadar on port 8765
cd /d "%~dp0"

echo.
echo ============================================
echo   TenderRadar - port 8765
echo   (8000/8001 may be cached as 2ndhand/Qasha)
echo ============================================
echo.

echo [1] Free ports 8765, 8000, 8001...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8765 ^| findstr LISTENING') do taskkill /PID %%a /F >nul 2>&1
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
echo OPEN IN A NEW BROWSER (Firefox) OR INCOGNITO:
echo   http://127.0.0.1:8765/health/
echo.
echo Must show plain text: TENDERRADAR OK
echo Then open: http://127.0.0.1:8765/
echo.
echo To test WITHOUT browser, run VERIFY.bat in another cmd window.
echo ============================================

python manage.py runserver 8765
