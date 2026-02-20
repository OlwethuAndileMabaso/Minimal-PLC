#!/usr/bin/env bash
# Install Minimal-PLC Runtime on Linux
set -e

echo "=== Minimal-PLC Linux Installer ==="
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update -qq
sudo apt-get install -y python3 python3-pip python3-venv git

# Install Python dependencies
echo "Installing Python packages..."
pip3 install -r "$REPO_DIR/runtime/requirements.txt"

# Install OpenPLC Runtime
echo "Installing OpenPLC Runtime..."
bash "$REPO_DIR/runtime/plc/openplc-runtime/install.sh"

echo ""
echo "Installation complete!"
echo "Run: cd runtime && bash start.sh"
