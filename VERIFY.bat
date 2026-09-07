@echo off
title Verify TenderRadar
cd /d "%~dp0"

powershell -NoProfile -Command "try { $r = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/health/' -UseBasicParsing -TimeoutSec 5; Write-Host 'STATUS:' $r.StatusCode; Write-Host $r.Content } catch { Write-Host 'FAILED - run: python manage.py runserver'; Write-Host $_.Exception.Message }"

pause
