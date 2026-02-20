# Minimal-PLC Runtime

The runtime module provides the web-based management interface for the Minimal-PLC platform.

## Features

- **Flask + Socket.IO** web server on port 8080
- **BACnet** device and point management
- **HMI Designer** integration (drag-and-drop)
- **User authentication** and role-based access
- **Data historian** with SQLite backend
- **Real-time** updates via WebSocket

## Starting the Server

```bash
cd Minimal-PLC
python runtime/webserver/server.py
```

## Install Scripts

| Script | Platform |
|--------|----------|
| `install-linux.sh` | Linux (Debian/Ubuntu) |
| `install-windows.bat` | Windows 10/11 |
| `install-mac.sh` | macOS 12+ |
