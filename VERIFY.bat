@echo off
title Verify TenderRadar server (no browser)
cd /d "%~dp0"

echo.
echo Testing TenderRadar WITHOUT browser...
echo.

powershell -NoProfile -Command "try { $r = Invoke-WebRequest -Uri 'http://127.0.0.1:8765/health/' -UseBasicParsing -TimeoutSec 5; Write-Host 'STATUS:' $r.StatusCode; Write-Host 'BODY:'; Write-Host $r.Content } catch { Write-Host 'FAILED - is RUN.bat running? Start RUN.bat first.'; Write-Host $_.Exception.Message }"

echo.
echo If you see TENDERRADAR OK above, Django works.
echo Your browser is showing cached 2ndhand/Qasha - NOT the server.
echo.
echo Fix browser: use a NEW browser OR Incognito OR clear site data for 127.0.0.1
echo.
pause
