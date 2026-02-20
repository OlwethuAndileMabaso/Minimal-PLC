@echo off
REM scripts/install-windows.bat — Install Minimal-PLC on Windows 10/11
SETLOCAL ENABLEDELAYEDEXPANSION

SET INSTALL_DIR=C:\MinimalPLC
SET REPO_DIR=%~dp0..
SET NSSM_URL=https://nssm.cc/release/nssm-2.24.zip
SET NSSM_ZIP=%TEMP%\nssm.zip
SET NSSM_DIR=%TEMP%\nssm

echo ===========================================
echo   Minimal-PLC -- Windows Installer
echo ===========================================

REM ── 1. Admin check ──────────────────────────────────────────────────────
net session >nul 2>&1
IF ERRORLEVEL 1 (
    echo ERROR: Please run this script as Administrator.
    pause
    exit /b 1
)

REM ── 2. Python check ─────────────────────────────────────────────────────
echo [1/5] Checking Python...
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ERROR: Python not found. Install from https://python.org
    pause
    exit /b 1
)

REM ── 3. Copy files ───────────────────────────────────────────────────────
echo [2/5] Copying application files...
IF NOT EXIST "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
xcopy /e /i /y "%REPO_DIR%\*" "%INSTALL_DIR%\" >nul

REM ── 4. Install Python dependencies ──────────────────────────────────────
echo [3/5] Installing Python dependencies...
python -m pip install --upgrade pip >nul
python -m pip install -r "%INSTALL_DIR%\runtime\requirements.txt"

REM ── 5. Initialise database ───────────────────────────────────────────────
echo [4/5] Initialising database...
cd /d "%INSTALL_DIR%"
python -c "import sys; sys.path.insert(0,'.'); from bridge.sql_historian import SQLHistorian; SQLHistorian('database/minimal_plc.db').initialize_db()"

REM ── 6. Register Windows Service via NSSM ────────────────────────────────
echo [5/5] Registering Windows Service...
where nssm >nul 2>&1
IF ERRORLEVEL 1 (
    echo Downloading NSSM...
    powershell -Command "Invoke-WebRequest '%NSSM_URL%' -OutFile '%NSSM_ZIP%'" >nul 2>&1
    powershell -Command "Expand-Archive '%NSSM_ZIP%' '%NSSM_DIR%'" >nul 2>&1
    copy /y "%NSSM_DIR%\nssm-2.24\win64\nssm.exe" "%SystemRoot%\System32\nssm.exe" >nul
)

nssm stop MinimalPLC >nul 2>&1
nssm remove MinimalPLC confirm >nul 2>&1
nssm install MinimalPLC python "%INSTALL_DIR%\runtime\webserver\server.py"
nssm set MinimalPLC AppDirectory "%INSTALL_DIR%"
nssm set MinimalPLC DisplayName "Minimal-PLC Industrial HMI"
nssm set MinimalPLC Start SERVICE_AUTO_START
nssm start MinimalPLC

echo.
echo ===========================================
echo   Minimal-PLC installed successfully!
echo   URL: http://localhost:8080
echo   Service: MinimalPLC
echo ===========================================
start http://localhost:8080
pause
ENDLOCAL
