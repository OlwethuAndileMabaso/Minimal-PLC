#!/usr/bin/env bash
# Install OpenPLC Runtime v3
set -e

RUNTIME_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_URL="https://github.com/thiagoralves/OpenPLC_v3.git"
CLONE_DIR="$RUNTIME_DIR/OpenPLC_v3"

if [ ! -d "$CLONE_DIR" ]; then
    echo "Cloning OpenPLC Runtime v3..."
    git clone "$REPO_URL" "$CLONE_DIR"
else
    echo "OpenPLC Runtime already cloned. Pulling latest..."
    git -C "$CLONE_DIR" pull
fi

cd "$CLONE_DIR"

if [ -f "install.sh" ]; then
    echo "Running OpenPLC Runtime installer..."
    bash install.sh linux
else
    echo "ERROR: install.sh not found in OpenPLC_v3 repository."
    exit 1
fi

echo ""
echo "OpenPLC Runtime installed successfully."
echo "Service should now be running on port 8181."
