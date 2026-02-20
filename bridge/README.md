# Bridge — BACnet, WebSocket and OpenPLC Integration

This directory contains the integration layer between the Minimal-PLC
platform and external systems.

| Module | Description |
|--------|-------------|
| `bacnet_discovery.py` | Discovers BACnet/IP devices using Who-Is / I-Am |
| `websocket_server.py` | Polls DB and emits live updates via Socket.IO |
| `openplc_client.py`   | HTTP client for OpenPLC Runtime REST API |
| `sql_historian.py`    | SQLite time-series historian |

## Running the BACnet Discovery Manually

```bash
python bridge/bacnet_discovery.py --interface eth0 --device-instance 999
```
