@echo off
REM TenderRadar - frontend setup (Desktop)
cd /d "%~dp0\frontend"

echo === TenderRadar frontend setup ===
echo.

if not exist .env.local (
  copy .env.local.example .env.local
  echo Created .env.local
)

call npm install
if errorlevel 1 goto error

echo.
echo === Done ===
echo Start frontend: npm run dev
echo Home page:      http://localhost:3000/
echo Signup page:    http://localhost:3000/signup
echo.
pause
goto end

:error
echo Setup failed. Check Node.js is installed.
pause

:end
