"""
BACnet/IP Property Reader

Reads present-value properties from BACnet objects on discovered devices.
"""

import asyncio
import json
import os
from typing import Any, Optional

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "config")


def load_bacnet_config() -> dict:
    path = os.path.join(CONFIG_DIR, "bacnet.json")
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


async def read_present_value(
    device_address: str,
    object_type: str,
    object_instance: int,
    local_device_id: int = 599,
) -> Optional[Any]:
    """
    Read the present-value of a single BACnet object.

    Args:
        device_address: BACnet device IP address (e.g. "192.168.1.100")
        object_type:    BACnet object type string (e.g. "analogInput")
        object_instance: BACnet object instance number
        local_device_id: Local BACnet device ID for this client

    Returns:
        The present-value, or None on error.
    """
    try:
        from bacpypes3.app import Application
        from bacpypes3.ipv4.app import NormalApplication
        from bacpypes3.local.device import DeviceObject
        from bacpypes3.pdu import Address
        from bacpypes3.primitivedata import ObjectIdentifier
    except ImportError:
        print("bacpypes3 not installed. Run: pip install bacpypes3")
        return None

    device_object = DeviceObject(
        objectIdentifier=ObjectIdentifier(("device", local_device_id)),
        objectName="Minimal-PLC-Reader",
        segmentationSupported="noSegmentation",
        maxApduLengthAccepted=1024,
    )

    try:
        async with NormalApplication(device_object) as app:
            value = await app.read_property(
                Address(device_address),
                ObjectIdentifier((object_type, object_instance)),
                "present-value",
            )
            return value
    except Exception as exc:
        print(f"Read error ({device_address} {object_type}:{object_instance}): {exc}")
        return None


async def poll_devices(devices: list, interval: float = 5.0) -> None:
    """
    Continuously poll a list of BACnet point definitions and print values.

    Each entry in `devices` should be:
        {"address": str, "object_type": str, "object_instance": int, "name": str}
    """
    config = load_bacnet_config()
    local_device_id = config.get("local_device_id", 599)

    while True:
        for point in devices:
            value = await read_present_value(
                point["address"],
                point["object_type"],
                point["object_instance"],
                local_device_id=local_device_id,
            )
            print(f"{point.get('name', point['object_type'])}:{point['object_instance']} = {value}")
        await asyncio.sleep(interval)


if __name__ == "__main__":
    config = load_bacnet_config()
    points = config.get("points", [])
    if not points:
        print("No points defined in config/bacnet.json")
    else:
        asyncio.run(poll_devices(points, interval=config.get("poll_interval_seconds", 5)))
