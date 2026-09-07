@echo off
title TenderRadar
cd /d "%~dp0"

echo.
echo ============================================
echo   TenderRadar
echo ============================================
echo.

if not exist .env copy .env.example .env >nul
python manage.py migrate >nul 2>&1

echo Starting server...
echo Open: http://127.0.0.1:8000/
echo ============================================

python manage.py runserver
