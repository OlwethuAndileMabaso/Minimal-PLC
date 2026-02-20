#!/usr/bin/env bash
# Start the Minimal-PLC runtime
set -e

RUNTIME_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$RUNTIME_DIR"

echo "Starting Minimal-PLC Runtime..."
python3 webserver/server.py &
echo $! > .runtime.pid
echo "Runtime started (PID: $(cat .runtime.pid))"
echo "Web interface: http://localhost:8080"
