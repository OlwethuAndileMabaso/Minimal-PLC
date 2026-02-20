#!/usr/bin/env bash
# editor/install.sh — Install OpenPLC Editor
set -e

EDITOR_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[Minimal-PLC] Installing OpenPLC Editor..."

# Clone OpenPLC Editor if not already present
if [ ! -d "$EDITOR_DIR/OpenPLC_Editor" ]; then
  git clone --depth=1 https://github.com/thiagoralves/OpenPLC_Editor.git \
    "$EDITOR_DIR/OpenPLC_Editor"
fi

cd "$EDITOR_DIR/OpenPLC_Editor"

# Install editor dependencies (Debian/Ubuntu)
if command -v apt-get &>/dev/null; then
  sudo apt-get install -y python3-wxgtk4.0 python3-pip 2>/dev/null || \
  sudo apt-get install -y python3-wxgtk3.0 python3-pip
fi

if [ -f requirements.txt ]; then
  pip3 install -r requirements.txt -q
fi

echo "[Minimal-PLC] OpenPLC Editor installed."
echo "Launch with: python OpenPLC_Editor/openplc_editor.py"
