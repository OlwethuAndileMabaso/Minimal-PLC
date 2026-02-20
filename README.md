# ⚡ Minimal-PLC

> Industrial SCADA/HMI Platform — Modern, open-source, and built for real-world industrial automation.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Angular](https://img.shields.io/badge/Angular-19-red.svg)](https://angular.io)
[![Node.js](https://img.shields.io/badge/Node.js-20+-green.svg)](https://nodejs.org)

---

## Features

| Feature | Description |
|---|---|
| 🎨 **HMI Designer** | Drag-and-drop canvas for building industrial screens |
| 📡 **BACnet/IP** | Native BACnet/IP device support (EasyIO, etc.) |
| 🔧 **Modbus TCP** | Modbus TCP for OpenPLC and industrial PLCs |
| 🔌 **OPC-UA** | OPC-UA device connectivity |
| 🚨 **Alarms** | Real-time alarm management with acknowledgment |
| 📈 **Trends** | Live and historical trend charts |
| 👥 **Users** | Role-based access (Admin, Operator, Viewer) |
| ⚙️ **Settings** | Full system configuration |
| 🔄 **Real-time** | Socket.io live data push |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Angular 19, Angular Material, TypeScript |
| Backend | Node.js, Express 4, Socket.io 4 |
| Database | SQLite 3 |
| Protocols | BACnet/IP, Modbus TCP, OPC-UA, MQTT |
| Charts | Chart.js 4 |
| Styling | SCSS, Inter font, CSS custom properties |

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/OlwethuAndileMabaso/Minimal-PLC.git
cd Minimal-PLC

# 2. Install all dependencies
npm run install:all

# 3. Start in development mode
npm run dev
```

Open your browser at **http://localhost:4200**

The API server runs at **http://localhost:3000**

---

## Project Structure

```
Minimal-PLC/
├── client/          ← Angular 19 frontend
│   └── src/app/
│       ├── welcome/        ← Startup/welcome screen
│       ├── layout/         ← Sidebar navigation shell
│       ├── dashboard/      ← Live dashboard
│       ├── hmi-designer/   ← Drag-and-drop HMI canvas
│       ├── devices/        ← Device management
│       ├── alarms/         ← Alarm management
│       ├── trends/         ← Trend charts
│       ├── users/          ← User management
│       └── settings/       ← System settings
├── server/          ← Node.js API + Socket.io server
├── docs/            ← Guides and documentation
└── scripts/         ← Install scripts for all platforms
```

---

## Screenshots

> _Screenshots coming soon — run the app and see for yourself!_

---

## Documentation

- [Getting Started](docs/getting-started.md)
- [Connecting EasyIO via BACnet](docs/connecting-easyio-bacnet.md)
- [Connecting OpenPLC via Modbus](docs/connecting-openplc.md)

---

## Install Scripts

| Platform | Command |
|---|---|
| Linux | `bash scripts/install-linux.sh` |
| Windows | `scripts\install-windows.bat` |
| macOS | `bash scripts/install-mac.sh` |

---

## License

MIT — see [LICENSE](LICENSE)

---

<p align="center">Built with ❤️ for industrial automation engineers</p>
