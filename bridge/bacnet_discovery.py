"""
bridge/bacnet_discovery.py
BACnet network discovery module for Minimal-PLC.

Uses bacpypes3 to broadcast Who-Is, collect I-Am responses,
read object lists, and persist results to the SQLite database.
"""

import asyncio
import json
import logging
import os
import sqlite3
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Repo root relative to this file
_REPO_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_DIR = _REPO_ROOT / "config"
_DB_PATH = _REPO_ROOT / "database" / "minimal_plc.db"


class BACnetDiscovery:
    """Discover BACnet devices on the local network and persist them to DB."""

    def __init__(self, interface: str = "eth0", device_instance: int = 999, port: int = 47808):
        self.interface = interface
        self.device_instance = device_instance
        self.port = port
        self._cfg = self.load_config()

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def load_config(self) -> dict:
        """Read config/bacnet.json and return as dict."""
        path = _CONFIG_DIR / "bacnet.json"
        try:
            with open(str(path), "r", encoding="utf-8") as fh:
                return json.load(fh)
        except FileNotFoundError:
            logger.warning("bacnet.json not found, using defaults.")
            return {}
        except json.JSONDecodeError as exc:
            logger.error("Invalid JSON in bacnet.json: %s", exc)
            return {}

    # ------------------------------------------------------------------
    # Database helpers
    # ------------------------------------------------------------------

    def _get_db(self) -> sqlite3.Connection:
        """Return a SQLite connection to the platform database."""
        os.makedirs(str(_DB_PATH.parent), exist_ok=True)
        conn = sqlite3.connect(str(_DB_PATH))
        conn.row_factory = sqlite3.Row
        return conn

    def save_devices_to_db(self, devices: list) -> None:
        """Persist a list of discovered device dicts to bacnet_devices."""
        if not devices:
            return
        conn = self._get_db()
        try:
            for dev in devices:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO bacnet_devices
                        (device_instance, name, ip_address, port, vendor, last_seen)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        dev.get("device_instance"),
                        dev.get("name", ""),
                        dev.get("ip_address", ""),
                        dev.get("port", self.port),
                        dev.get("vendor", ""),
                        datetime.utcnow().isoformat(),
                    ),
                )
            conn.commit()
            logger.info("Saved %d devices to DB.", len(devices))
        except Exception as exc:
            logger.error("Error saving devices: %s", exc)
        finally:
            conn.close()

    def save_points_to_db(self, points: list) -> None:
        """Persist a list of BACnet point dicts to bacnet_points."""
        if not points:
            return
        conn = self._get_db()
        try:
            for pt in points:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO bacnet_points
                        (device_id, object_type, object_instance, name,
                         description, unit, last_value, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        pt.get("device_id"),
                        pt.get("object_type", ""),
                        pt.get("object_instance", 0),
                        pt.get("name", ""),
                        pt.get("description", ""),
                        pt.get("unit", ""),
                        pt.get("last_value"),
                        datetime.utcnow().isoformat(),
                    ),
                )
            conn.commit()
            logger.info("Saved %d points to DB.", len(points))
        except Exception as exc:
            logger.error("Error saving points: %s", exc)
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # BACnet async methods
    # ------------------------------------------------------------------

    async def scan_devices(self) -> list:
        """
        Broadcast a Who-Is and collect I-Am responses.

        Returns a list of device info dicts.
        """
        devices = []
        try:
            from bacpypes3.app import Application
            from bacpypes3.pdu import Address
            from bacpypes3.primitivedata import ObjectIdentifier
            from bacpypes3.apdu import WhoIsRequest

            timeout = self._cfg.get("scan_timeout_seconds", 30)

            app = await Application.create(
                {
                    "objectName": "Minimal-PLC-Discovery",
                    "objectIdentifier": f"device,{self.device_instance}",
                    "maxApduLengthAccepted": self._cfg.get("max_apdu_length", 1024),
                }
            )

            responses = []

            async def _collect(apdu):
                responses.append(apdu)

            app.i_am_callback = _collect

            # Send Who-Is broadcast
            await app.who_is()
            await asyncio.sleep(timeout)

            for apdu in responses:
                try:
                    dev_id = int(str(apdu.iAmDeviceIdentifier).split(",")[1])
                    ip = str(apdu.pduSource)
                    devices.append(
                        {
                            "device_instance": dev_id,
                            "name": f"Device-{dev_id}",
                            "ip_address": ip.split(":")[0] if ":" in ip else ip,
                            "port": self.port,
                            "vendor": "",
                        }
                    )
                except Exception as exc:
                    logger.debug("Error parsing I-Am response: %s", exc)

            await app.close()
        except ImportError:
            logger.warning("bacpypes3 not installed — BACnet scan skipped.")
        except Exception as exc:
            logger.error("BACnet scan error: %s", exc)

        self.save_devices_to_db(devices)
        return devices

    async def read_device_objects(self, device_id: int, ip: str) -> list:
        """
        Read the object-list property of a BACnet device.

        Returns a list of (object_type, object_instance) tuples.
        """
        try:
            from bacpypes3.app import Application
            from bacpypes3.pdu import Address
            from bacpypes3.primitivedata import ObjectIdentifier

            app = await Application.create(
                {
                    "objectName": "Minimal-PLC-Reader",
                    "objectIdentifier": f"device,{self.device_instance}",
                }
            )
            address = Address(ip)
            result = await app.read_property(
                address,
                ObjectIdentifier("device", device_id),
                "object-list",
            )
            await app.close()
            return list(result) if result else []
        except Exception as exc:
            logger.error("Error reading objects from device %d: %s", device_id, exc)
            return []

    async def read_present_value(
        self, device_id: int, obj_type: str, obj_instance: int
    ):
        """Read the present-value of a single BACnet object."""
        try:
            from bacpypes3.app import Application
            from bacpypes3.pdu import Address
            from bacpypes3.primitivedata import ObjectIdentifier

            conn = self._get_db()
            row = conn.execute(
                "SELECT ip_address FROM bacnet_devices WHERE device_instance=?",
                (device_id,),
            ).fetchone()
            conn.close()
            if not row:
                logger.warning("Device %d not found in DB.", device_id)
                return None

            app = await Application.create(
                {
                    "objectName": "Minimal-PLC-Reader",
                    "objectIdentifier": f"device,{self.device_instance}",
                }
            )
            address = Address(row["ip_address"])
            result = await app.read_property(
                address,
                ObjectIdentifier(obj_type, obj_instance),
                "present-value",
            )
            await app.close()
            return result
        except Exception as exc:
            logger.error(
                "Error reading present-value %s:%d from device %d: %s",
                obj_type,
                obj_instance,
                device_id,
                exc,
            )
            return None


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="BACnet discovery tool")
    parser.add_argument("--interface", default="eth0")
    parser.add_argument("--device-instance", type=int, default=999)
    parser.add_argument("--port", type=int, default=47808)
    args = parser.parse_args()

    disc = BACnetDiscovery(
        interface=args.interface,
        device_instance=args.device_instance,
        port=args.port,
    )
    devices = asyncio.run(disc.scan_devices())
    print(f"Found {len(devices)} device(s):")
    for d in devices:
        print(f"  [{d['device_instance']}] {d['name']} @ {d['ip_address']}")
