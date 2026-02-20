# BACnet Integration Guide

## Overview

Minimal-PLC uses **bacpypes3** to communicate with BACnet/IP devices on your local network.

---

## Configuration

Edit `config/bacnet.json`:

```json
{
  "local_device_id": 599,
  "interface": "auto",
  "poll_interval_seconds": 5,
  "points": [
    {
      "name": "AHU-1 Supply Temp",
      "address": "192.168.1.10",
      "object_type": "analogInput",
      "object_instance": 1
    },
    {
      "name": "AHU-1 Fan Status",
      "address": "192.168.1.10",
      "object_type": "binaryInput",
      "object_instance": 3
    }
  ]
}
```

| Field | Description |
|-------|-------------|
| `local_device_id` | BACnet device ID for this Minimal-PLC client (must be unique on your network) |
| `interface` | Network interface IP or `"auto"` to detect automatically |
| `poll_interval_seconds` | How often to read all points |
| `points` | List of BACnet objects to poll |

---

## Discovering Devices

Run the discovery script to find BACnet devices on your network:

```bash
cd runtime
python3 bacnet/discovery.py
```

Example output:
```
Found 2 device(s):
  Device 1001 at 192.168.1.10
  Device 1002 at 192.168.1.11
```

---

## Supported Object Types

Any standard BACnet object type supported by bacpypes3, including:

- `analogInput` / `analogOutput` / `analogValue`
- `binaryInput` / `binaryOutput` / `binaryValue`
- `multiStateInput` / `multiStateOutput` / `multiStateValue`

---

## Troubleshooting

**No devices found**
- Ensure your firewall allows UDP port 47808
- Confirm BACnet devices are on the same subnet (or that BACnet routing is configured)

**Read errors**
- Check that the object type and instance number are correct
- Some devices require a confirmed Who-Is before they respond to reads
