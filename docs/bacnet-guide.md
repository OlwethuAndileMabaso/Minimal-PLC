# BACnet Integration Guide

## What is BACnet?

BACnet (Building Automation and Control Networks) is an ASHRAE, ANSI, and ISO standard
data communication protocol for building automation and control systems.
Minimal-PLC uses **BACnet/IP** (Annex J) via the `bacpypes3` Python library.

---

## Supported Object Types

| Object Type | Description |
|-------------|-------------|
| Analog Input (AI) | Sensor readings (temperature, pressure, etc.) |
| Analog Output (AO) | Actuator setpoints |
| Analog Value (AV) | Software analog values |
| Binary Input (BI) | Digital sensor states |
| Binary Output (BO) | Digital output states |
| Binary Value (BV) | Software binary values |
| Multi-State Input | Enumerated sensor states |
| Multi-State Output | Enumerated output states |

---

## Configuration

Edit `config/bacnet.json`:

```json
{
  "enabled": true,
  "interface": "eth0",
  "device_instance": 999,
  "port": 47808,
  "bbmd_address": "",
  "bbmd_ttl": 900,
  "max_apdu_length": 1024,
  "scan_timeout_seconds": 30
}
```

| Key | Description |
|-----|-------------|
| `interface` | Network interface name (`eth0`, `en0`, `Wi-Fi`) |
| `device_instance` | Unique BACnet device instance (1–4194302) |
| `port` | BACnet/IP port (default 47808) |
| `bbmd_address` | BBMD address for inter-subnet routing (leave blank for local) |
| `scan_timeout_seconds` | Time to wait for I-Am responses |

---

## Network Discovery

1. Go to **BACnet Points** in the sidebar
2. Click **Scan Network**
3. The platform broadcasts a Who-Is request and waits for I-Am responses
4. Discovered devices appear in the Devices table
5. Points are read automatically and appear in the Points table
6. Each point shows: Name, Type, Present Value, Unit, Device, Last Updated

### Manual Scan (CLI)

```bash
python bridge/bacnet_discovery.py --interface eth0 --device-instance 999
```

---

## Point Alarms

In the database, each `bacnet_points` row has `alarm_low` and `alarm_high` columns.
When the WebSocket bridge polls a point, it checks these thresholds and emits
an `alarm` Socket.IO event if the value is out of range.

To set thresholds, update the database directly or via a future UI:

```sql
UPDATE bacnet_points
SET alarm_low = 10.0, alarm_high = 90.0
WHERE name = 'Temperature_Zone1';
```

---

## Troubleshooting

| Problem | Solution |
|---------|---------|
| No devices found | Check `interface` name; ensure BACnet devices are on the same subnet or BBMD is configured |
| Scan times out immediately | Ensure `bacpypes3` is installed: `pip install bacpypes3` |
| Permission denied on socket | Run as root or grant CAP_NET_BIND_SERVICE |
| Values not updating | Check that poll_interval_seconds in platform.json > 0 and WebSocket is connected |
