@echo off
title TenderRadar - Setup and Run
cd /d "%~dp0"

echo.
echo ============================================
echo   TenderRadar - fixing folder and starting
echo ============================================
echo.

REM --- Kill anything on port 8000 (2ndhand / old servers) ---
echo [1/5] Freeing port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
  echo   Stopping PID %%a
  taskkill /PID %%a /F >nul 2>&1
)
timeout /t 1 /nobreak >nul

REM --- Sync with GitHub ---
echo [2/5] Syncing with GitHub main...
git merge --abort >nul 2>&1
git fetch origin
if errorlevel 1 (
  echo   Git fetch failed - check internet connection
  goto fail
)
git reset --hard origin/main
if errorlevel 1 goto fail

REM --- Verify this is TenderRadar ---
findstr /C:"TenderRadar.settings" manage.py >nul || (
  echo [FAIL] This folder is not TenderRadar!
  goto fail
)
if not exist static\css\tenderradar.css (
  echo [FAIL] Missing TenderRadar UI files after sync.
  goto fail
)
findstr /S /I /M "2ndhand" manage.py tenders\*.py templates\*.html 2>nul && (
  echo [FAIL] 2ndhand code found - wrong project folder!
  goto fail
)
echo   [OK] TenderRadar folder verified

REM --- Install deps ---
echo [3/5] Installing Python packages...
pip install -r requirements.txt -q
if errorlevel 1 (
  echo   pip install failed
  goto fail
)

if not exist .env copy .env.example .env >nul

echo [4/5] Database migrate...
python manage.py migrate --fake-initial >nul 2>&1
python manage.py migrate >nul 2>&1

echo [5/5] Starting TenderRadar...
echo.
echo   OPEN IN INCOGNITO:  http://127.0.0.1:8000/
echo   (NOT a bookmark - type the URL fresh)
echo.
echo   You should see: TenderRadar - SA Tender Discovery
echo   NOT 2ndhand / pawn shop
echo.
echo   Press Ctrl+C to stop the server
echo ============================================
echo.

python manage.py runserver
goto end

:fail
echo.
echo Setup failed. Clone fresh:
echo   cd C:\Users\Admin\Desktop
echo   git clone https://github.com/Kamo2330/TenderRadar.git TenderRadar_new
echo.
pause
exit /b 1

:end
