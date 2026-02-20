@echo off
REM Install Minimal-PLC Runtime on Windows
echo === Minimal-PLC Windows Installer ===

SET REPO_DIR=%~dp0..

REM Check Python
python --version 2>nul || (echo ERROR: Python not found. Install from https://python.org && exit /b 1)

REM Install Python dependencies
echo Installing Python packages...
pip install -r "%REPO_DIR%\runtime\requirements.txt"

echo.
echo Installation complete!
echo Run: cd runtime ^& start.bat
