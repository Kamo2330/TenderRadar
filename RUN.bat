@echo off
title TenderRadar on port 8001
cd /d "%~dp0"

echo.
echo ============================================
echo   TenderRadar - port 8001 (avoids Qasha/2ndhand on 8000)
echo ============================================
echo.

echo [1] Killing anything on ports 8000 and 8001...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /PID %%a /F >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8001 ^| findstr LISTENING') do taskkill /PID %%a /F >nul 2>&1

echo [2] Installing correct package versions...
pip install "django>=6.0,<6.1" "djangorestframework>=3.18,<4" -r requirements.txt -q
if errorlevel 1 (
  echo pip install failed
  pause
  exit /b 1
)

python -c "import django; import rest_framework; print('Django', django.get_version(), '| DRF', rest_framework.VERSION)"
if errorlevel 1 (
  echo Package check failed
  pause
  exit /b 1
)

if not exist .env copy .env.example .env >nul
python manage.py migrate --fake-initial >nul 2>&1
python manage.py migrate >nul 2>&1

echo.
echo [3] Starting on http://127.0.0.1:8001/
echo.
echo OPEN IN INCOGNITO:
echo   http://127.0.0.1:8001/health/
echo   must say: TENDERRADAR OK
echo.
echo Then: http://127.0.0.1:8001/
echo.
echo (Port 8000 may be Qasha - do NOT use 8000)
echo ============================================
echo.

python manage.py runserver 8001
