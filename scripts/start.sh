#!/usr/bin/env bash
# scripts/start.sh — Start Minimal-PLC on Linux/macOS
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$SCRIPT_DIR/.."

# Try systemd first, else start directly
if command -v systemctl &>/dev/null && systemctl is-enabled minimal-plc &>/dev/null 2>&1; then
  echo "Starting Minimal-PLC via systemd..."
  sudo systemctl start minimal-plc
  echo "Started. URL: http://localhost:8080"
else
  echo "Starting Minimal-PLC directly..."
  VENV="$REPO_DIR/venv/bin/python"
  if [ ! -f "$VENV" ]; then
    VENV="python3"
  fi
  cd "$REPO_DIR"
  exec "$VENV" runtime/webserver/server.py
fi
