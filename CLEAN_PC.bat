@echo off
title Delete old TenderRadar folders and clone clean copy
cd /d C:\Users\Admin\Desktop

echo.
echo This deletes OLD TenderRadar folders on this PC:
echo   Desktop\TenderRadar
echo   Desktop\TenderRadar_LIVE
echo   Desktop\TenderRadar_NEW
echo.
echo Then it clones a clean copy from GitHub.
echo.
pause

if exist TenderRadar rmdir /s /q TenderRadar
if exist TenderRadar_LIVE rmdir /s /q TenderRadar_LIVE
if exist TenderRadar_NEW rmdir /s /q TenderRadar_NEW

git clone https://github.com/Kamo2330/TenderRadar.git TenderRadar
if errorlevel 1 (
  echo Clone failed. Check internet or Git install.
  pause
  exit /b 1
)

cd TenderRadar
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env >nul
python manage.py migrate
python manage.py load_sample_tenders

echo.
echo Clean copy is ready at C:\Users\Admin\Desktop\TenderRadar
echo Next: python manage.py runserver
echo Then open Incognito: http://127.0.0.1:8000/
echo Health must say: UI: clean-v5
echo.
pause
