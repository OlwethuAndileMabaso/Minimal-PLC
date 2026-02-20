"""
bridge/websocket_server.py
Real-time WebSocket bridge for Minimal-PLC.

Polls bacnet_points from SQLite every `poll_interval` seconds
and emits 'point_update' / 'alarm' events via Flask-SocketIO.
"""

import logging
import sqlite3
import threading
import time
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

_DB_PATH = Path(__file__).resolve().parent.parent / "database" / "minimal_plc.db"


class WebSocketBridge:
    """
    Background bridge that periodically reads BACnet points from the
    SQLite historian and broadcasts live updates to connected HMI clients.
    """

    def __init__(self, socketio, poll_interval: int = 5):
        """
        Parameters
        ----------
        socketio : flask_socketio.SocketIO
            The SocketIO instance to emit events on.
        poll_interval : int
            Polling interval in seconds.
        """
        self._socketio = socketio
        self._poll_interval = poll_interval
        self._running = False
        self._thread: threading.Thread | None = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Start the background polling thread."""
        if self._running:
            logger.debug("WebSocketBridge already running.")
            return
        self._running = True
        self._thread = threading.Thread(
            target=self._poll_loop, daemon=True, name="ws-bridge-poll"
        )
        self._thread.start()
        logger.info("WebSocketBridge started (interval=%ds).", self._poll_interval)

    def stop(self) -> None:
        """Stop the background polling thread gracefully."""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=self._poll_interval + 2)
        logger.info("WebSocketBridge stopped.")

    # ------------------------------------------------------------------
    # Internal loop
    # ------------------------------------------------------------------

    def _poll_loop(self) -> None:
        """Main loop: poll DB → emit updates → check alarms → sleep."""
        while self._running:
            try:
                points = self._get_points_from_db()
                for point in points:
                    # Emit live value update
                    self._socketio.emit("point_update", dict(point))
                    # Check alarms
                    alarm = self._check_alarms(point)
                    if alarm:
                        self._socketio.emit("alarm", alarm)
            except Exception as exc:
                logger.error("Poll loop error: %s", exc)
            time.sleep(self._poll_interval)

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------

    def _get_points_from_db(self) -> list:
        """Return all bacnet_points rows as a list of dicts."""
        try:
            conn = sqlite3.connect(str(_DB_PATH))
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT id, name, last_value, unit, last_updated, "
                "alarm_low, alarm_high, object_type "
                "FROM bacnet_points"
            ).fetchall()
            conn.close()
            return [dict(r) for r in rows]
        except sqlite3.OperationalError:
            # DB or table may not exist yet during first run
            return []
        except Exception as exc:
            logger.error("Error reading points from DB: %s", exc)
            return []

    # ------------------------------------------------------------------
    # Alarm checking
    # ------------------------------------------------------------------

    def _check_alarms(self, point: dict) -> dict | None:
        """
        Compare the point's last_value against alarm thresholds.

        Returns an alarm dict if a threshold is breached, else None.
        """
        value = point.get("last_value")
        if value is None:
            return None

        try:
            val = float(value)
        except (TypeError, ValueError):
            return None

        alarm_high = point.get("alarm_high")
        alarm_low = point.get("alarm_low")

        if alarm_high is not None and val > float(alarm_high):
            return {
                "point_id": point["id"],
                "point_name": point.get("name", ""),
                "alarm_type": "HIGH",
                "message": f"{point.get('name','')} value {val} exceeds high limit {alarm_high}",
                "severity": "high",
                "timestamp": datetime.utcnow().isoformat(),
            }

        if alarm_low is not None and val < float(alarm_low):
            return {
                "point_id": point["id"],
                "point_name": point.get("name", ""),
                "alarm_type": "LOW",
                "message": f"{point.get('name','')} value {val} below low limit {alarm_low}",
                "severity": "high",
                "timestamp": datetime.utcnow().isoformat(),
            }

        return None
