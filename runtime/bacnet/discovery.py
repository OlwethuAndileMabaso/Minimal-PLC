"""
BACnet/IP Device Discovery

Discovers BACnet devices on the local network using a Who-Is broadcast.
"""

import asyncio
import json
import os

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "config")


def load_bacnet_config() -> dict:
    path = os.path.join(CONFIG_DIR, "bacnet.json")
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


async def discover_devices(timeout: float = 5.0) -> list:
    """
    Send a BACnet Who-Is broadcast and collect I-Am responses.

    Returns a list of dicts: [{"device_id": int, "address": str}, ...]
    """
    try:
        from bacpypes3.app import Application
        from bacpypes3.ipv4.app import NormalApplication
        from bacpypes3.local.device import DeviceObject
        from bacpypes3.pdu import Address
        from bacpypes3.primitivedata import ObjectIdentifier
    except ImportError:
        print("bacpypes3 not installed. Run: pip install bacpypes3")
        return []

    config = load_bacnet_config()
    local_device_id = config.get("local_device_id", 599)
    interface = config.get("interface", "")

    device_object = DeviceObject(
        objectIdentifier=ObjectIdentifier(("device", local_device_id)),
        objectName="Minimal-PLC-Discovery",
        segmentationSupported="noSegmentation",
        maxApduLengthAccepted=1024,
    )

    discovered = []

    try:
        address = Address(interface) if interface and interface != "auto" else None
        async with NormalApplication(device_object, address) as app:

            def i_am_callback(apdu):
                device_id = int(apdu.iAmDeviceIdentifier[1])
                address_str = str(apdu.pduSource)
                discovered.append({"device_id": device_id, "address": address_str})

            app.i_am_indication = i_am_callback
            app.who_is()
            await asyncio.sleep(timeout)
    except Exception as exc:
        print(f"Discovery error: {exc}")

    return discovered


if __name__ == "__main__":
    devices = asyncio.run(discover_devices())
    print(f"Found {len(devices)} device(s):")
    for d in devices:
        print(f"  Device {d['device_id']} at {d['address']}")
