@echo off
REM Reset Desktop folder to match GitHub TenderRadar (fixes wrong/old/2nd-bantu mix)
cd /d "%~dp0"
echo.
echo === Reset TenderRadar to GitHub main ===
echo This replaces ALL files in this folder with GitHub version.
echo.
pause

git merge --abort 2>nul
git fetch origin
git reset --hard origin/main

if errorlevel 1 (
  echo.
  echo Git reset failed. Clone fresh instead:
  echo   cd C:\Users\Admin\Desktop
  echo   ren TenderRadar TenderRadar_old
  echo   git clone https://github.com/Kamo2330/TenderRadar.git
  pause
  exit /b 1
)

echo.
echo [OK] Folder now matches GitHub.
echo.
pip install -r requirements.txt
if not exist .env copy .env.example .env
echo.
echo Run:  python manage.py runserver
echo Open:  http://127.0.0.1:8000/
echo Use INCOGNITO window if browser still shows old 2nd Bantu site.
echo.
pause
