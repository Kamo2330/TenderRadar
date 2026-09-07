@echo off
title TenderRadar
cd /d "%~dp0"

if not exist .env copy .env.example .env >nul
python manage.py migrate >nul 2>&1
python manage.py load_sample_tenders >nul 2>&1

echo Open http://127.0.0.1:8000/

python manage.py runserver
