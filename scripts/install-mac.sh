#!/usr/bin/env bash
# Install Minimal-PLC Runtime on macOS
set -e

echo "=== Minimal-PLC macOS Installer ==="
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Check for Homebrew
if ! command -v brew &>/dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install dependencies
echo "Installing system dependencies..."
brew install python3 git

# Install Python dependencies
echo "Installing Python packages..."
pip3 install -r "$REPO_DIR/runtime/requirements.txt"

echo ""
echo "Installation complete!"
echo "Run: cd runtime && bash start.sh"
