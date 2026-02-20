@echo off
REM scripts/start.bat — Start Minimal-PLC on Windows
echo Starting Minimal-PLC...
net start MinimalPLC >nul 2>&1
IF ERRORLEVEL 1 (
    echo Service not found, starting directly...
    cd /d "%~dp0.."
    python runtime\webserver\server.py
) ELSE (
    echo Minimal-PLC started. URL: http://localhost:8080
)
