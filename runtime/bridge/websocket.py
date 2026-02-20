"""
WebSocket Bridge

Bridges live BACnet / PLC data to connected browser clients via SocketIO.
"""

import asyncio
import json
import os
import threading
import time

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "config")


def load_bacnet_config() -> dict:
    path = os.path.join(CONFIG_DIR, "bacnet.json")
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


class DataBridge:
    """
    Polls BACnet points at a configurable interval and emits values
    to all connected SocketIO clients.
    """

    def __init__(self, socketio):
        self.socketio = socketio
        self.config = load_bacnet_config()
        self.points = self.config.get("points", [])
        self.interval = self.config.get("poll_interval_seconds", 5)
        self._running = False
        self._thread: threading.Thread | None = None

    def start(self):
        """Start the polling thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the polling thread."""
        self._running = False

    def _poll_loop(self):
        """Background thread: poll BACnet and emit to clients."""
        from bacnet.reader import read_present_value

        while self._running:
            for point in self.points:
                try:
                    value = asyncio.run(
                        read_present_value(
                            point["address"],
                            point["object_type"],
                            point["object_instance"],
                        )
                    )
                    self.socketio.emit(
                        "data_update",
                        {
                            "name": point.get("name", f"{point['object_type']}:{point['object_instance']}"),
                            "value": value,
                            "timestamp": time.time(),
                        },
                    )
                except Exception:
                    pass
            time.sleep(self.interval)
