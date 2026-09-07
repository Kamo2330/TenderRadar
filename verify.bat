@echo off
REM Quick check: is this the real TenderRadar from GitHub?
cd /d "%~dp0"
echo.
echo === TenderRadar folder check ===
echo Folder: %CD%
echo.

if not exist manage.py (
  echo [FAIL] manage.py not found - wrong folder!
  goto end
)

echo --- Git (latest commit) ---
git log --oneline -1 2>nul || echo [WARN] Not a git repo
echo.

echo --- Django version in requirements.txt ---
findstr django requirements.txt 2>nul || echo [FAIL] requirements.txt missing - OLD COPY
echo.

echo --- New UI files (must exist) ---
if exist static\css\tenderradar.css (echo [OK] static\css\tenderradar.css) else (echo [FAIL] static\css\tenderradar.css MISSING - need git pull)
if exist static\js\tenderradar.js (echo [OK] static\js\tenderradar.js) else (echo [FAIL] static\js\tenderradar.js MISSING)
echo.

echo --- URLs (login should REDIRECT to home, not auth urls) ---
findstr /C:"RedirectView" TenderRadar\urls.py 2>nul && echo [OK] Login redirect configured || echo [FAIL] Old urls.py - still has login wall
findstr /C:"django.contrib.auth.urls" TenderRadar\urls.py 2>nul && echo [FAIL] Still includes auth urls - OLD CODE || echo [OK] No auth urls include
echo.

echo --- Dashboard (should NOT require login) ---
findstr /C:"Public tender dashboard" tenders\views.py 2>nul && echo [OK] Public dashboard || echo [FAIL] Old views.py - login still required
echo.

echo === If you see FAIL above, run fix-desktop.bat ===
echo.

:end
pause
