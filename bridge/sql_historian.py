"""
bridge/sql_historian.py
SQLite historian for Minimal-PLC.

Logs time-series point values, retrieves history, and performs
scheduled retention cleanup.
"""

import logging
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCHEMA_PATH = _REPO_ROOT / "database" / "schema.sql"


class SQLHistorian:
    """
    Manages the Minimal-PLC SQLite time-series database.

    Parameters
    ----------
    db_path : str or Path
        Path to the SQLite database file.
    """

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = str(_REPO_ROOT / "database" / "minimal_plc.db")
        self.db_path = str(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    # ------------------------------------------------------------------
    # Connection
    # ------------------------------------------------------------------

    def get_connection(self) -> sqlite3.Connection:
        """Return an open SQLite connection with row_factory set."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def initialize_db(self) -> None:
        """
        Execute schema.sql to create all tables (if they do not exist).
        Also inserts the default admin user.
        """
        try:
            with open(str(_SCHEMA_PATH), "r", encoding="utf-8") as fh:
                schema = fh.read()
        except FileNotFoundError:
            logger.error("schema.sql not found at %s", _SCHEMA_PATH)
            return

        conn = self.get_connection()
        try:
            conn.executescript(schema)
            conn.commit()
            logger.info("Database initialised from schema.sql")
        except Exception as exc:
            logger.error("Error initialising DB: %s", exc)
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Writing
    # ------------------------------------------------------------------

    def log_point(self, point_id: int, value: float, quality: str = "good") -> bool:
        """
        Insert a time-series record into point_history.

        Parameters
        ----------
        point_id : int
            FK to bacnet_points.id
        value : float
            Measured value.
        quality : str
            Data quality string, e.g. ``good``, ``bad``, ``uncertain``.

        Returns
        -------
        bool
            True on success.
        """
        conn = self.get_connection()
        try:
            conn.execute(
                "INSERT INTO point_history (point_id, value, quality, timestamp) VALUES (?, ?, ?, ?)",
                (point_id, value, quality, datetime.utcnow().isoformat()),
            )
            # Also update last_value on the point
            conn.execute(
                "UPDATE bacnet_points SET last_value=?, last_updated=? WHERE id=?",
                (value, datetime.utcnow().isoformat(), point_id),
            )
            conn.commit()
            return True
        except Exception as exc:
            logger.error("log_point error: %s", exc)
            return False
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Reading
    # ------------------------------------------------------------------

    def get_history(self, point_id: int, hours: int = 24) -> list:
        """
        Return time-series records for a given point over the past N hours.

        Parameters
        ----------
        point_id : int
            FK to bacnet_points.id
        hours : int
            Look-back window in hours.

        Returns
        -------
        list of dict
        """
        since = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
        conn = self.get_connection()
        try:
            rows = conn.execute(
                "SELECT timestamp, value, quality FROM point_history "
                "WHERE point_id=? AND timestamp>=? ORDER BY timestamp ASC",
                (point_id, since),
            ).fetchall()
            return [dict(r) for r in rows]
        except Exception as exc:
            logger.error("get_history error: %s", exc)
            return []
        finally:
            conn.close()

    def get_all_points_latest(self) -> list:
        """
        Return the latest value for every BACnet point.

        Returns
        -------
        list of dict
        """
        conn = self.get_connection()
        try:
            rows = conn.execute(
                "SELECT p.id, p.name, p.last_value, p.unit, p.last_updated, "
                "d.name AS device_name "
                "FROM bacnet_points p "
                "LEFT JOIN bacnet_devices d ON p.device_id=d.id "
                "ORDER BY p.name"
            ).fetchall()
            return [dict(r) for r in rows]
        except Exception as exc:
            logger.error("get_all_points_latest error: %s", exc)
            return []
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def cleanup_old_records(self, days: int = 30) -> int:
        """
        Delete point_history records older than `days` days.

        Returns
        -------
        int
            Number of rows deleted.
        """
        cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
        conn = self.get_connection()
        try:
            cur = conn.execute(
                "DELETE FROM point_history WHERE timestamp < ?", (cutoff,)
            )
            conn.commit()
            deleted = cur.rowcount
            logger.info("Cleaned up %d old records (older than %d days).", deleted, days)
            return deleted
        except Exception as exc:
            logger.error("cleanup_old_records error: %s", exc)
            return 0
        finally:
            conn.close()
