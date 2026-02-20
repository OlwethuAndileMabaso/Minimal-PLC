#!/usr/bin/env bash
# runtime/install-linux.sh — Install Minimal-PLC Runtime on Linux (Debian/Ubuntu)
set -e

INSTALL_DIR="/opt/minimal-plc"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "[Minimal-PLC] Installing runtime on Linux..."

# Ensure running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root: sudo bash runtime/install-linux.sh"
  exit 1
fi

echo "[1/4] Installing system dependencies..."
apt-get update -qq
apt-get install -y python3 python3-pip python3-venv sqlite3

echo "[2/4] Setting up virtual environment..."
python3 -m venv "$INSTALL_DIR/venv"
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip -q
"$INSTALL_DIR/venv/bin/pip" install -r "$REPO_DIR/runtime/requirements.txt" -q

echo "[3/4] Initialising database..."
"$INSTALL_DIR/venv/bin/python" - <<'PYEOF'
import sqlite3, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from bridge.sql_historian import SQLHistorian
h = SQLHistorian('/opt/minimal-plc/database/minimal_plc.db')
h.initialize_db()
PYEOF

echo "[4/4] Done. Start with: sudo systemctl start minimal-plc"
echo "[Minimal-PLC] Runtime installed at $INSTALL_DIR"
