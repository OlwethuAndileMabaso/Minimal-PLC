# Runtime

This directory contains everything that runs **24/7 on the target machine**.

## Components

| Directory | Description |
|-----------|-------------|
| `webserver/` | Flask web server (port 8080) — serves the HMI and management dashboard |
| `plc/` | OpenPLC Runtime — executes IEC 61131-3 PLC programs |
| `bacnet/` | BACnet/IP client — reads live values from BACnet devices on the network |
| `bridge/` | WebSocket bridge and data historian |
| `database/` | SQLite schema for history, alarms, and configuration |

## Requirements

- Python 3.9+
- See `requirements.txt` for Python packages

## Quick Start

### Linux / macOS

```bash
pip3 install -r requirements.txt
bash start.sh
```

### Windows

```bat
pip install -r requirements.txt
start.bat
```

The web interface is available at **http://localhost:8080**

## Stopping

```bash
bash stop.sh   # Linux/macOS
stop.bat       # Windows
```
