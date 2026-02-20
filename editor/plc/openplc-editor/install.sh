#!/usr/bin/env bash
# Install OpenPLC Editor
set -e

EDITOR_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_URL="https://github.com/thiagoralves/OpenPLC_Editor.git"
CLONE_DIR="$EDITOR_DIR/OpenPLC_Editor"

if [ ! -d "$CLONE_DIR" ]; then
    echo "Cloning OpenPLC Editor..."
    git clone "$REPO_URL" "$CLONE_DIR"
else
    echo "OpenPLC Editor already cloned. Pulling latest..."
    git -C "$CLONE_DIR" pull
fi

cd "$CLONE_DIR"

if [ -f "install.sh" ]; then
    echo "Running OpenPLC Editor installer..."
    bash install.sh
else
    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt 2>/dev/null || true
fi

echo ""
echo "OpenPLC Editor installed successfully."
echo "To launch: cd $CLONE_DIR && python3 openplc_editor.py"
