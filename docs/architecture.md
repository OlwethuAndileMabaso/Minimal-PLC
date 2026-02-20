# Architecture

## Overview

Minimal-PLC is split into two independent parts:

```
EDITOR (engineering PC)
├── hmi/designer/     Freeboard drag-and-drop HMI designer
└── plc/              OpenPLC Editor — IEC 61131-3 programming

        ↓ Deploy over LAN

RUNTIME (target machine — Linux or Windows)
├── webserver/        Flask + SocketIO server (port 8080)
├── plc/              OpenPLC Runtime — executes PLC program
├── bacnet/           BACnet/IP client — reads field devices
├── bridge/           WebSocket bridge + data historian
└── database/         SQLite — history, alarms, config
```

---

## Web Server (`runtime/webserver/server.py`)

- Framework: **Flask 3** + **Flask-SocketIO**
- Async mode: **eventlet**
- Routes:
  - `/` → redirect to `/dashboard`
  - `/dashboard` — system status overview
  - `/bacnet` — BACnet device list
  - `/network` — network settings
  - `/settings` — platform configuration
  - `/hmi` — Freeboard HMI (served from `runtime/webserver/hmi/`)
- Config loaded from `config/platform.json`

---

## BACnet Client (`runtime/bacnet/`)

- Library: **bacpypes3**
- `discovery.py` — sends Who-Is broadcast, collects I-Am responses
- `reader.py` — reads `present-value` from BACnet objects

---

## Bridge (`runtime/bridge/`)

- `websocket.py` — polls BACnet on a background thread, emits `data_update` events via SocketIO
- `historian.py` — writes values to SQLite history table

---

## Database (`runtime/database/schema.sql`)

Three tables:
- `history` — time-series values for each point
- `alarms` — alarm events with acknowledgement tracking
- `config` — key/value runtime configuration store

---

## Configuration

All configuration is in `config/`:

| File | Purpose |
|------|---------|
| `platform.json` | Server host, port, debug flag |
| `network.json` | Network interface settings |
| `bacnet.json` | BACnet local device ID, points list |
