@echo off
REM Start the Minimal-PLC runtime
echo Starting Minimal-PLC Runtime...
cd /d "%~dp0"
start /b python webserver\server.py
echo Runtime started.
echo Web interface: http://localhost:8080
