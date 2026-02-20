#!/usr/bin/env bash
# runtime/install-mac.sh — Install Minimal-PLC Runtime on macOS
set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
INSTALL_DIR="$HOME/MinimalPLC"

echo "[Minimal-PLC] Installing runtime on macOS..."

# Install Homebrew if missing
if ! command -v brew &>/dev/null; then
  echo "Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

echo "[1/3] Installing dependencies via Homebrew..."
brew install python3 sqlite3 2>/dev/null || true

echo "[2/3] Setting up virtual environment..."
mkdir -p "$INSTALL_DIR"
python3 -m venv "$INSTALL_DIR/venv"
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip -q
"$INSTALL_DIR/venv/bin/pip" install -r "$REPO_DIR/runtime/requirements.txt" -q

echo "[3/3] Done."
echo "[Minimal-PLC] Start with: python runtime/webserver/server.py"
