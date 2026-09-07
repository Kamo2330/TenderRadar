@echo off
REM TenderRadar - one-click backend setup (Desktop)
cd /d "%~dp0"

echo === TenderRadar backend setup ===
echo.

pip install -r requirements.txt
if errorlevel 1 goto error

if not exist .env (
  copy .env.example .env
  echo Created .env from .env.example
)

python manage.py migrate --fake-initial
if errorlevel 1 (
  echo migrate --fake-initial failed, trying normal migrate...
  python manage.py migrate
)

echo.
echo === Done ===
echo Start backend:  python manage.py runserver
echo Open site:      http://127.0.0.1:8000/
echo.
pause
goto end

:error
echo Setup failed. Check Python is installed and you are in the TenderRadar folder.
pause

:end
