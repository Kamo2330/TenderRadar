@echo off
title Clone TenderRadar FRESH (fixes wrong folder + 2ndhand cache)
echo.
echo This creates a NEW folder: TenderRadar_LIVE
echo Your old TenderRadar folder is left untouched.
echo.

cd /d C:\Users\Admin\Desktop

REM Kill port 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /PID %%a /F >nul 2>&1

if exist TenderRadar_LIVE (
  echo Removing old TenderRadar_LIVE...
  rmdir /S /Q TenderRadar_LIVE
)

echo Cloning from GitHub...
git clone https://github.com/Kamo2330/TenderRadar.git TenderRadar_LIVE
if errorlevel 1 (
  echo Clone failed. Check internet and Git install.
  pause
  exit /b 1
)

cd TenderRadar_LIVE

echo Installing packages...
pip install -r requirements.txt
copy .env.example .env >nul
python manage.py migrate --fake-initial >nul 2>&1
python manage.py migrate >nul 2>&1

echo.
echo ============================================
echo   SUCCESS - Starting TenderRadar_LIVE
echo ============================================
echo.
echo STEP 1: Test this URL in INCOGNITO first:
echo         http://127.0.0.1:8000/health/
echo.
echo You MUST see plain text:
echo         TENDERRADAR OK
echo         Django 6.x
echo.
echo If you see 2ndhand instead, your BROWSER is cached - not Django.
echo.
echo STEP 2: Then open:  http://127.0.0.1:8000/
echo.
echo Press Ctrl+C to stop server
echo ============================================
echo.

start "" cmd /c "timeout /t 3 /nobreak >nul && start msedge -inprivate http://127.0.0.1:8000/health/"

python manage.py runserver
