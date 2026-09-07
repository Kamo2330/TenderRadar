@echo off
REM Find why you see 2ndhand instead of TenderRadar
echo.
echo ====== 1. Which folder am I in? ======
cd /d "%~dp0"
echo %CD%
echo.

echo ====== 2. Is this TenderRadar? (must say TenderRadar) ======
findstr DJANGO_SETTINGS_MODULE manage.py 2>nul || echo [FAIL] No manage.py here!
echo.

echo ====== 3. Any 2ndhand code in this folder? (should find NOTHING) ======
findstr /S /I /M "2ndhand pawn Get cash now" *.* 2>nul
if errorlevel 1 (echo [OK] No 2ndhand text in this folder) else (echo [FAIL] THIS FOLDER IS THE WRONG PROJECT!)
echo.

echo ====== 4. TenderRadar UI files present? ======
if exist static\css\tenderradar.css (echo [OK] tenderradar.css) else (echo [FAIL] Missing - run fix-desktop.bat)
echo.

echo ====== 5. What is using port 8000? ======
netstat -ano | findstr :8000
echo.
echo If you see a PID above, kill it:  taskkill /PID number /F
echo.

echo ====== 6. Test Django directly (start server in OTHER window first) ======
echo Run in another cmd:  python manage.py runserver
echo Then open ONLY:  http://127.0.0.1:8000/
echo Use Incognito - NOT a bookmark!
echo.
pause
