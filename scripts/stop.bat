@echo off
REM scripts/stop.bat — Stop Minimal-PLC on Windows
echo Stopping Minimal-PLC...
net stop MinimalPLC >nul 2>&1
IF ERRORLEVEL 1 (
    echo MinimalPLC service not found or not running.
) ELSE (
    echo Minimal-PLC stopped.
)
