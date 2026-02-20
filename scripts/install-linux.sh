#!/usr/bin/env bash
# scripts/install-linux.sh — Install Minimal-PLC on Linux (Debian/Ubuntu)
set -e

INSTALL_DIR="/opt/minimal-plc"
SERVICE_FILE="/etc/systemd/system/minimal-plc.service"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "========================================="
echo "  Minimal-PLC — Linux Installer"
echo "========================================="

# ── 1. Root check ──────────────────────────────────────────────────────────
if [ "$EUID" -ne 0 ]; then
  echo "ERROR: Please run as root: sudo bash scripts/install-linux.sh"
  exit 1
fi

# ── 2. System dependencies ─────────────────────────────────────────────────
echo "[1/6] Installing system dependencies..."
apt-get update -qq
apt-get install -y python3 python3-pip python3-venv sqlite3 chromium-browser 2>/dev/null || \
  apt-get install -y python3 python3-pip python3-venv sqlite3 chromium 2>/dev/null || \
  apt-get install -y python3 python3-pip python3-venv sqlite3

# ── 3. Create service user ─────────────────────────────────────────────────
echo "[2/6] Creating service user..."
id -u minimalplc &>/dev/null || useradd -r -s /bin/false -d "$INSTALL_DIR" minimalplc

# ── 4. Install application files ───────────────────────────────────────────
echo "[3/6] Installing application files..."
mkdir -p "$INSTALL_DIR"
cp -r "$REPO_DIR"/. "$INSTALL_DIR/"
chown -R minimalplc:minimalplc "$INSTALL_DIR"

# ── 5. Python virtual environment ──────────────────────────────────────────
echo "[4/6] Setting up Python virtual environment..."
python3 -m venv "$INSTALL_DIR/venv"
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip -q
"$INSTALL_DIR/venv/bin/pip" install -r "$INSTALL_DIR/runtime/requirements.txt" -q

# ── 6. Initialise database ─────────────────────────────────────────────────
echo "[5/6] Initialising database..."
sudo -u minimalplc "$INSTALL_DIR/venv/bin/python" -c "
import sys; sys.path.insert(0,'$INSTALL_DIR')
from bridge.sql_historian import SQLHistorian
SQLHistorian('$INSTALL_DIR/database/minimal_plc.db').initialize_db()
"

# ── 7. Systemd service ─────────────────────────────────────────────────────
echo "[6/6] Installing systemd service..."
cp "$REPO_DIR/scripts/minimal-plc.service" "$SERVICE_FILE"
sed -i "s|/opt/minimal-plc|$INSTALL_DIR|g" "$SERVICE_FILE"
systemctl daemon-reload
systemctl enable minimal-plc
systemctl restart minimal-plc

echo ""
echo "✅ Minimal-PLC installed successfully!"
echo "   URL: http://localhost:8080"
echo "   Status: sudo systemctl status minimal-plc"
echo "   Logs:   sudo journalctl -u minimal-plc -f"
