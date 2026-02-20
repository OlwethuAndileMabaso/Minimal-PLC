"""
bridge/openplc_client.py
HTTP client for the OpenPLC Runtime REST API.

Wraps the OpenPLC v3 web interface endpoints so that Minimal-PLC can
read/write PLC variables, start/stop programs, and query runtime status.
"""

import logging
from typing import Any

import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

_DEFAULT_TIMEOUT = 5  # seconds


class OpenPLCClient:
    """
    Client for the OpenPLC Runtime HTTP API.

    Parameters
    ----------
    host : str
        Hostname or IP of the OpenPLC web server.
    port : int
        TCP port of the OpenPLC web server (default 8080).
    token : str
        API / session token for authenticated requests.
    """

    def __init__(self, host: str = "localhost", port: int = 8080, token: str = ""):
        self.base_url = f"http://{host}:{port}"
        self._token = token
        self._session = requests.Session()
        if token:
            self._session.headers.update({"Authorization": f"Bearer {token}"})

    # ------------------------------------------------------------------
    # Connection check
    # ------------------------------------------------------------------

    def is_connected(self) -> bool:
        """Return True if the OpenPLC server is reachable."""
        try:
            resp = self._session.get(
                f"{self.base_url}/", timeout=_DEFAULT_TIMEOUT
            )
            return resp.status_code < 500
        except RequestException:
            return False

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def get_status(self) -> dict:
        """
        Query the OpenPLC runtime status.

        Returns
        -------
        dict
            Keys: ``running`` (bool), ``program`` (str), ``uptime`` (int seconds).
        """
        try:
            resp = self._session.get(
                f"{self.base_url}/runtime/status", timeout=_DEFAULT_TIMEOUT
            )
            resp.raise_for_status()
            return resp.json()
        except RequestException as exc:
            logger.warning("get_status failed: %s", exc)
            return {"running": False, "program": "", "uptime": 0}

    # ------------------------------------------------------------------
    # Variables
    # ------------------------------------------------------------------

    def get_variables(self) -> list:
        """
        Return all PLC variables.

        Returns
        -------
        list of dict
            Each dict has ``name``, ``type``, and ``value`` keys.
        """
        try:
            resp = self._session.get(
                f"{self.base_url}/runtime/variables", timeout=_DEFAULT_TIMEOUT
            )
            resp.raise_for_status()
            return resp.json()
        except RequestException as exc:
            logger.warning("get_variables failed: %s", exc)
            return []

    def read_variable(self, name: str) -> Any:
        """
        Read a single PLC variable by name.

        Parameters
        ----------
        name : str
            Variable name (e.g. ``QX0.0``).

        Returns
        -------
        The variable value, or None on error.
        """
        try:
            resp = self._session.get(
                f"{self.base_url}/runtime/variable/{name}",
                timeout=_DEFAULT_TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("value")
        except RequestException as exc:
            logger.warning("read_variable(%s) failed: %s", name, exc)
            return None

    def write_variable(self, name: str, value: Any) -> bool:
        """
        Write a value to a PLC variable.

        Returns
        -------
        bool
            True on success.
        """
        try:
            resp = self._session.post(
                f"{self.base_url}/runtime/variable/{name}",
                json={"value": value},
                timeout=_DEFAULT_TIMEOUT,
            )
            resp.raise_for_status()
            return True
        except RequestException as exc:
            logger.warning("write_variable(%s=%s) failed: %s", name, value, exc)
            return False

    # ------------------------------------------------------------------
    # PLC control
    # ------------------------------------------------------------------

    def start_plc(self) -> bool:
        """Send the start command to OpenPLC Runtime."""
        try:
            resp = self._session.post(
                f"{self.base_url}/runtime/start", timeout=_DEFAULT_TIMEOUT
            )
            resp.raise_for_status()
            logger.info("OpenPLC start command sent.")
            return True
        except RequestException as exc:
            logger.error("start_plc failed: %s", exc)
            return False

    def stop_plc(self) -> bool:
        """Send the stop command to OpenPLC Runtime."""
        try:
            resp = self._session.post(
                f"{self.base_url}/runtime/stop", timeout=_DEFAULT_TIMEOUT
            )
            resp.raise_for_status()
            logger.info("OpenPLC stop command sent.")
            return True
        except RequestException as exc:
            logger.error("stop_plc failed: %s", exc)
            return False
