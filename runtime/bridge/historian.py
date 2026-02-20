"""
Data Historian

Records BACnet / PLC values to the SQLite database for trend and alarm history.
"""

import os
import sqlite3
import time
from typing import Any, Optional

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "database")
DB_PATH = os.path.join(DB_DIR, "historian.sqlite")
SCHEMA_PATH = os.path.join(DB_DIR, "schema.sql")


def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection, creating the database if needed."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    _ensure_schema(conn)
    return conn


def _ensure_schema(conn: sqlite3.Connection) -> None:
    """Create tables from schema.sql if they don't already exist."""
    if os.path.exists(SCHEMA_PATH):
        with open(SCHEMA_PATH) as f:
            conn.executescript(f.read())
        conn.commit()


def record_value(point_name: str, value: Any, quality: str = "good") -> None:
    """Insert a single data point into the history table."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO history (point_name, value, quality, ts) VALUES (?, ?, ?, ?)",
            (point_name, str(value), quality, time.time()),
        )
        conn.commit()


def get_history(
    point_name: str,
    limit: int = 1000,
    since: Optional[float] = None,
) -> list:
    """
    Retrieve historical values for a named point.

    Args:
        point_name: The point to query.
        limit:      Maximum number of rows to return (newest first).
        since:      Optional Unix timestamp — only return rows after this time.

    Returns:
        List of dicts with keys: id, point_name, value, quality, ts.
    """
    with get_connection() as conn:
        if since is not None:
            rows = conn.execute(
                "SELECT * FROM history WHERE point_name = ? AND ts >= ?"
                " ORDER BY ts DESC LIMIT ?",
                (point_name, since, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM history WHERE point_name = ? ORDER BY ts DESC LIMIT ?",
                (point_name, limit),
            ).fetchall()
    return [dict(row) for row in rows]


def record_alarm(point_name: str, message: str, severity: str = "warning") -> None:
    """Insert an alarm event into the alarms table."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO alarms (point_name, message, severity, ts) VALUES (?, ?, ?, ?)",
            (point_name, message, severity, time.time()),
        )
        conn.commit()
