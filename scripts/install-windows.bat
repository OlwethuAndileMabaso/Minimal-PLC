@echo off
echo Installing Minimal-PLC...
where node >nul 2>&1 || (echo Node.js not found. Please install from https://nodejs.org && pause && exit)
call npm run install:all
echo.
echo Done! Run: npm run dev
pause
