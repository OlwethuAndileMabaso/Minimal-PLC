# Architecture

## Overview

Minimal-PLC is a layered platform that combines a Python web server,
a BACnet discovery engine, a real-time WebSocket bridge, and a drag-and-drop
HMI designer into a single deployable application.

---

## Component Diagram

```
┌───────────────────────────────────────────────────────────────────┐
│                        MINIMAL-PLC PLATFORM                       │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │               Flask Web Server  (port 8080)                  │ │
│  │                                                              │ │
│  │  Pages:  /dashboard  /programs  /bacnet  /hmi               │ │
│  │          /network    /database  /users                       │ │
│  │                                                              │ │
│  │  API:    /api/status            /api/bacnet/points          │ │
│  │          /api/bacnet/discover   /api/config/*               │ │
│  │          /api/hmi/layout        /api/hmi/deploy             │ │
│  └──────────────────────┬──────────────────────────────────────┘ │
│                         │ Flask-SocketIO (eventlet)               │
│  ┌──────────────────────▼──────────────────────────────────────┐ │
│  │                  WebSocket Bridge                            │ │
│  │   • Polls bacnet_points every 5 s                           │ │
│  │   • Emits  point_update  events                             │ │
│  │   • Emits  alarm         events                             │ │
│  └──────────────────────┬──────────────────────────────────────┘ │
│                         │                                         │
│  ┌──────────────────────▼──────────────────────────────────────┐ │
│  │                  SQLite Historian                            │ │
│  │   • bacnet_devices    • bacnet_points                       │ │
│  │   • point_history     • alarms                              │ │
│  │   • users             • network_config                      │ │
│  │   • audit_log         • projects                            │ │
│  └──────────────────────┬──────────────────────────────────────┘ │
│                         │                                         │
│  ┌──────────────────────▼──────────────────────────────────────┐ │
│  │                  BACnet Discovery Engine                     │ │
│  │   • Who-Is / I-Am broadcast (bacpypes3)                     │ │
│  │   • Read object-list and present-value                      │ │
│  │   • Saves devices + points to SQLite                        │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─────────────────────────┐   ┌─────────────────────────────┐  │
│  │  HMI Designer            │   │  HMI Runtime (kiosk)        │  │
│  │  /hmi/designer/          │   │  /hmi/runtime               │  │
│  │  • Drag-and-drop canvas  │   │  • Loads deployed layout    │  │
│  │  • Widget palette        │   │  • Socket.IO live updates   │  │
│  │  • Properties panel      │   │  • Alarm banners            │  │
│  │  • Deploy via API        │   │  • Touch-friendly           │  │
│  └─────────────────────────┘   └─────────────────────────────┘  │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  OpenPLC Client (optional)                                   │ │
│  │  • GET/POST variables    • Start / Stop PLC program         │ │
│  └─────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
        ▲  Browser                    ▲  Android / iOS
        │  http://localhost:8080      │  WebView → /hmi/runtime
```

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Web server | Python 3, Flask 3, Flask-SocketIO, eventlet |
| Real-time | Socket.IO 4 (WebSocket) |
| BACnet | bacpypes3 |
| Database | SQLite 3 (WAL mode) |
| Frontend | Bootstrap 5, Font Awesome 6 |
| HMI Designer | Vanilla JS, HTML5 Drag and Drop API |
| Android | Java, WebView, AppCompat |
| iOS | Swift, WKWebView |

---

## Data Flow

```
BACnet Device → [Who-Is/I-Am] → BACnetDiscovery → SQLite
                                                      ↓
Browser ← [Socket.IO point_update] ← WebSocketBridge ← polling

Browser → [POST /api/hmi/deploy] → network_config(hmi_deployed_layout)
HMI Runtime → [GET /api/hmi/layout] → renders widgets → live values
```

---

## Security Notes

- The `secret_key` in `config/platform.json` **must** be changed before production deployment.
- The default admin password (`admin`) **must** be changed immediately after first login.
- `usesCleartextTraffic: true` (Android) and `NSAllowsArbitraryLoads: true` (iOS) are set
  to allow HTTP access on local networks. For production, enable HTTPS and update these settings.
