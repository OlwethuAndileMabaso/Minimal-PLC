@echo off
REM runtime/install-windows.bat — Install Minimal-PLC Runtime on Windows
SETLOCAL

SET INSTALL_DIR=C:\MinimalPLC
SET REPO_DIR=%~dp0..

echo [Minimal-PLC] Installing runtime on Windows...

REM Check Python
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python not found. Please install Python 3.8+ from https://python.org
    exit /b 1
)

echo [1/3] Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r "%REPO_DIR%\runtime\requirements.txt"

echo [2/3] Initialising database...
python -c "import sys; sys.path.insert(0,'%REPO_DIR%'); from bridge.sql_historian import SQLHistorian; SQLHistorian('%INSTALL_DIR%\\database\\minimal_plc.db').initialize_db()"

echo [3/3] Done.
echo [Minimal-PLC] Start with: python runtime\webserver\server.py
ENDLOCAL
