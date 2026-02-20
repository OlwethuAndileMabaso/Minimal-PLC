#!/usr/bin/env bash
# scripts/install-mac.sh — Install Minimal-PLC on macOS
set -e

INSTALL_DIR="$HOME/MinimalPLC"
PLIST_DIR="$HOME/Library/LaunchAgents"
PLIST_FILE="$PLIST_DIR/com.minimalplc.plist"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "========================================="
echo "  Minimal-PLC — macOS Installer"
echo "========================================="

# ── 1. Homebrew ────────────────────────────────────────────────────────────
echo "[1/5] Checking Homebrew..."
if ! command -v brew &>/dev/null; then
  echo "Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# ── 2. System dependencies ─────────────────────────────────────────────────
echo "[2/5] Installing dependencies..."
brew install python3 sqlite3 2>/dev/null || true

# ── 3. Copy files ──────────────────────────────────────────────────────────
echo "[3/5] Installing application files..."
mkdir -p "$INSTALL_DIR"
cp -r "$REPO_DIR"/. "$INSTALL_DIR/"

# ── 4. Virtual environment ─────────────────────────────────────────────────
echo "[4/5] Setting up Python virtual environment..."
python3 -m venv "$INSTALL_DIR/venv"
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip -q
"$INSTALL_DIR/venv/bin/pip" install -r "$INSTALL_DIR/runtime/requirements.txt" -q

# Initialise database
"$INSTALL_DIR/venv/bin/python" -c "
import sys; sys.path.insert(0,'$INSTALL_DIR')
from bridge.sql_historian import SQLHistorian
SQLHistorian('$INSTALL_DIR/database/minimal_plc.db').initialize_db()
"

# ── 5. LaunchAgent ─────────────────────────────────────────────────────────
echo "[5/5] Installing launchd agent..."
mkdir -p "$PLIST_DIR"
cat > "$PLIST_FILE" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.minimalplc</string>
  <key>ProgramArguments</key>
  <array>
    <string>$INSTALL_DIR/venv/bin/python</string>
    <string>$INSTALL_DIR/runtime/webserver/server.py</string>
  </array>
  <key>WorkingDirectory</key>
  <string>$INSTALL_DIR</string>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>$INSTALL_DIR/minimal-plc.log</string>
  <key>StandardErrorPath</key>
  <string>$INSTALL_DIR/minimal-plc-error.log</string>
</dict>
</plist>
PLIST

launchctl unload "$PLIST_FILE" 2>/dev/null || true
launchctl load "$PLIST_FILE"

sleep 2
open http://localhost:8080

echo ""
echo "✅ Minimal-PLC installed successfully!"
echo "   URL:    http://localhost:8080"
echo "   Logs:   tail -f $INSTALL_DIR/minimal-plc.log"
echo "   Stop:   launchctl unload $PLIST_FILE"
