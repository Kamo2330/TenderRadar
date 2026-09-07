@echo off
title Verify TenderRadar
cd /d "%~dp0"

echo.
echo Checking TenderRadar server...
echo.

powershell -NoProfile -Command "try { $r = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/health/' -UseBasicParsing -TimeoutSec 5; Write-Host $r.Content; if ($r.Content -match 'UI: table-v3') { Write-Host ''; Write-Host 'OK - You have the NEW UI code.' -ForegroundColor Green } else { Write-Host ''; Write-Host 'OLD CODE - Run UPDATE.bat then restart server.' -ForegroundColor Red } } catch { Write-Host 'FAILED - Start server first: python manage.py runserver'; Write-Host $_.Exception.Message }"

echo.
pause
