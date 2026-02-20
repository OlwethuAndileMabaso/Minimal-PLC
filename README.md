# ⚡ Minimal-PLC

> **Open-source Industrial HMI + PLC Platform**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS%20%7C%20Android%20%7C%20iOS-blue)](README.md)
[![Python](https://img.shields.io/badge/python-3.8%2B-green)](runtime/requirements.txt)

Minimal-PLC is a free, open-source industrial HMI and PLC platform that combines OpenPLC Runtime, a BACnet discovery engine, a real-time WebSocket bridge, and a Freeboard-based HMI designer into one unified platform.

---

## Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| Linux    | ✅     | Full support — recommended for production |
| Windows  | ✅     | Full support via Windows Service (NSSM) |
| macOS    | ✅     | Full support via launchd |
| Android  | ✅     | HMI viewer (WebView app) |
| iOS      | ✅     | HMI viewer (WKWebView app) |
| Browser  | ✅     | Any modern browser, no install required |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MINIMAL-PLC PLATFORM                 │
│                                                         │
│  ┌──────────────┐    ┌─────────────────────────────┐   │
│  │ OpenPLC      │    │  Flask Web Server (port 8080)│   │
│  │ Runtime      │◄──►│  - Dashboard                 │   │
│  │ (optional)   │    │  - BACnet Manager            │   │
│  └──────────────┘    │  - HMI Designer              │   │
│                      │  - Programs                  │   │
│  ┌──────────────┐    │  - Users / Config            │   │
│  │ BACnet       │    └─────────┬───────────────────┘   │
│  │ Discovery    │              │ Socket.IO               │
│  │ Engine       │    ┌─────────▼───────────────────┐   │
│  └──────┬───────┘    │  WebSocket Bridge            │   │
│         │            │  - Real-time point updates   │   │
│  ┌──────▼───────┐    │  - Alarm events              │   │
│  │ SQLite       │◄──►│  - PLC variable sync         │   │
│  │ Historian    │    └─────────────────────────────┘   │
│  └──────────────┘                                       │
│                      ┌─────────────────────────────┐   │
│                      │  HMI Runtime (fullscreen)    │   │
│                      │  - Drag-and-drop designer    │   │
│                      │  - Live data widgets         │   │
│                      │  - Tablet / mobile ready     │   │
│                      └─────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
         ▲                          ▲
         │                          │
   ┌─────┴──────┐          ┌────────┴──────┐
   │  Android   │          │    iOS        │
   │  HMI App   │          │  HMI App      │
   └────────────┘          └───────────────┘
```

---

## Quick Start

### Linux

```bash
git clone https://github.com/OlwethuAndileMabaso/Minimal-PLC.git
cd Minimal-PLC
sudo bash scripts/install-linux.sh
```

Open your browser: **http://localhost:8080**

### Windows

```bat
git clone https://github.com/OlwethuAndileMabaso/Minimal-PLC.git
cd Minimal-PLC
scripts\install-windows.bat
```

### macOS

```bash
git clone https://github.com/OlwethuAndileMabaso/Minimal-PLC.git
cd Minimal-PLC
bash scripts/install-mac.sh
```

### Manual Start (any platform)

```bash
cd Minimal-PLC
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r runtime/requirements.txt
python runtime/webserver/server.py
```

### Android / iOS

1. Build the app from `mobile/android/` or `mobile/ios/`
2. Enter your server IP when prompted (e.g. `192.168.1.100:8080`)
3. The app opens the HMI runtime in fullscreen landscape mode

---

## Folder Structure

```
Minimal-PLC/
├── runtime/          ← Flask web server + HTML templates
├── editor/           ← OpenPLC Editor integration
├── hmi/              ← HMI designer and runtime
├── bridge/           ← BACnet discovery, WebSocket bridge, OPC client
├── database/         ← SQLite schema
├── config/           ← Platform, network, BACnet configuration
├── scripts/          ← Install and start/stop scripts
├── mobile/           ← Android and iOS HMI viewer apps
└── docs/             ← Documentation
```

---

## Default Login

| Username | Password | Role  |
|----------|----------|-------|
| admin    | admin    | Admin |

> **Change the default password immediately after first login.**

---

## Credits

- **OpenPLC Runtime** — [thiagoralves/OpenPLC_v3](https://github.com/thiagoralves/OpenPLC_v3) (GPL-3.0)
- **OpenPLC Editor** — [thiagoralves/OpenPLC_Editor](https://github.com/thiagoralves/OpenPLC_Editor) (GPL-2.0)
- **Freeboard HMI** — [Freeboard/freeboard](https://github.com/Freeboard/freeboard) (MIT)

---

## License

[MIT License](LICENSE) © 2026 OlwethuAndileMabaso / Minimal-PLC Contributors
