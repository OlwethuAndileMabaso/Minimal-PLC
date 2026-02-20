@echo off
REM Stop the Minimal-PLC runtime
echo Stopping Minimal-PLC Runtime...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq server.py" 2>nul
echo Runtime stopped.
