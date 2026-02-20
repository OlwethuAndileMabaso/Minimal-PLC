#!/usr/bin/env bash
# scripts/stop.sh — Stop Minimal-PLC on Linux/macOS
set -e

if command -v systemctl &>/dev/null && systemctl is-active minimal-plc &>/dev/null 2>&1; then
  echo "Stopping Minimal-PLC via systemd..."
  sudo systemctl stop minimal-plc
  echo "Stopped."
else
  # Find and kill the server process
  PID=$(pgrep -f "runtime/webserver/server.py" 2>/dev/null || true)
  if [ -n "$PID" ]; then
    echo "Stopping Minimal-PLC (PID $PID)..."
    kill "$PID"
    echo "Stopped."
  else
    echo "Minimal-PLC is not running."
  fi
fi
