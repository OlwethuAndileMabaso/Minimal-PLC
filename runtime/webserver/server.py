"""
runtime/webserver/server.py
Flask + Socket.IO web server for the Minimal-PLC platform.

Routes
------
GET  /                   → redirect to /dashboard
GET  /dashboard          → main dashboard
GET  /programs           → PLC program management
GET  /bacnet             → BACnet point manager
GET  /network            → network / settings page
GET  /database           → data history viewer
GET  /users              → user management
GET  /hmi                → HMI designer host page
GET  /hmi/runtime        → fullscreen HMI kiosk

API
---
GET/POST /api/status
GET      /api/bacnet/points
POST     /api/bacnet/discover
GET/POST /api/config/network
GET/POST /api/config/bacnet
GET/POST /api/hmi/layout
POST     /api/hmi/deploy
"""

import json
import logging
import os
import sqlite3
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    jsonify,
    send_from_directory,
    url_for,
)
from flask_login import LoginManager, UserMixin, login_required
from flask_socketio import SocketIO, emit

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # repo root
CONFIG_DIR = BASE_DIR / "config"
DB_PATH = BASE_DIR / "database" / "minimal_plc.db"
HMI_DESIGNER = BASE_DIR / "hmi" / "designer"
HMI_RUNTIME = BASE_DIR / "hmi" / "runtime"

# ---------------------------------------------------------------------------
# Load platform configuration
# ---------------------------------------------------------------------------
def load_config(name: str) -> dict:
    """Load a JSON config file from the config/ directory."""
    path = CONFIG_DIR / name
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        logging.warning("Config file not found: %s", path)
        return {}
    except json.JSONDecodeError as exc:
        logging.error("Invalid JSON in %s: %s", path, exc)
        return {}


platform_cfg = load_config("platform.json")
WEB_PORT = platform_cfg.get("web_port", 8080)
SECRET_KEY = platform_cfg.get("secret_key", "change-this-in-production")
DEBUG = platform_cfg.get("debug", False)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("minimal-plc")

# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------
app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = SECRET_KEY

socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")
login_manager = LoginManager(app)
login_manager.login_view = "dashboard"  # type: ignore[assignment]

# ---------------------------------------------------------------------------
# SQLite helper
# ---------------------------------------------------------------------------

def get_db() -> sqlite3.Connection:
    """Return a SQLite connection to the platform database."""
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def query_db(sql: str, args: tuple = (), one: bool = False):
    """Execute a SELECT query and return rows."""
    conn = get_db()
    try:
        cur = conn.execute(sql, args)
        rows = cur.fetchall()
        return (rows[0] if rows else None) if one else rows
    except Exception as exc:
        logger.error("DB query error: %s", exc)
        return None if one else []
    finally:
        conn.close()


def execute_db(sql: str, args: tuple = ()) -> bool:
    """Execute an INSERT / UPDATE / DELETE statement."""
    conn = get_db()
    try:
        conn.execute(sql, args)
        conn.commit()
        return True
    except Exception as exc:
        logger.error("DB execute error: %s", exc)
        return False
    finally:
        conn.close()

# ---------------------------------------------------------------------------
# Simple user model (no full auth required for demo)
# ---------------------------------------------------------------------------

class User(UserMixin):
    def __init__(self, user_id, username, role):
        self.id = user_id
        self.username = username
        self.role = role


@login_manager.user_loader
def load_user(user_id):
    row = query_db("SELECT id, username, role FROM users WHERE id=?", (user_id,), one=True)
    if row:
        return User(row["id"], row["username"], row["role"])
    return None

# ---------------------------------------------------------------------------
# Page routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    plc_status = "STOPPED"
    point_count = 0
    alarm_count = 0
    uptime = "N/A"
    try:
        rows = query_db("SELECT COUNT(*) AS cnt FROM bacnet_points")
        point_count = rows[0]["cnt"] if rows else 0
        arows = query_db(
            "SELECT COUNT(*) AS cnt FROM alarms WHERE acknowledged_at IS NULL"
        )
        alarm_count = arows[0]["cnt"] if arows else 0
    except Exception:
        pass
    alarms = query_db(
        "SELECT a.triggered_at, p.name, a.message, a.severity "
        "FROM alarms a LEFT JOIN bacnet_points p ON a.point_id=p.id "
        "ORDER BY a.triggered_at DESC LIMIT 10"
    ) or []
    return render_template(
        "dashboard.html",
        plc_status=plc_status,
        point_count=point_count,
        alarm_count=alarm_count,
        uptime=uptime,
        alarms=alarms,
    )


@app.route("/programs")
def programs():
    return render_template("programs.html")


@app.route("/bacnet")
def bacnet():
    return render_template("bacnet.html")


@app.route("/network")
def network():
    net_cfg = load_config("network.json")
    bacnet_cfg = load_config("bacnet.json")
    plc_cfg = platform_cfg.get("openplc", {})
    return render_template(
        "network.html",
        net_cfg=net_cfg,
        bacnet_cfg=bacnet_cfg,
        plc_cfg=plc_cfg,
        platform_cfg=platform_cfg,
    )


@app.route("/database")
def database():
    return render_template("database.html")


@app.route("/users")
def users():
    user_list = query_db(
        "SELECT id, username, role, email, last_login, active FROM users ORDER BY username"
    ) or []
    return render_template("users.html", users=user_list)


@app.route("/hmi")
def hmi():
    return render_template("hmi.html")


@app.route("/hmi/runtime")
def hmi_runtime():
    return send_from_directory(str(HMI_RUNTIME), "index.html")


@app.route("/hmi/designer/")
@app.route("/hmi/designer")
def hmi_designer():
    return send_from_directory(str(HMI_DESIGNER), "index.html")

# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------

@app.route("/api/status", methods=["GET", "POST"])
def api_status():
    if request.method == "POST":
        return jsonify({"ok": True})
    return jsonify(
        {
            "platform": platform_cfg.get("platform_name", "Minimal-PLC"),
            "version": platform_cfg.get("version", "1.0.0"),
            "plc_status": "STOPPED",
            "timestamp": datetime.utcnow().isoformat(),
        }
    )


@app.route("/api/bacnet/points", methods=["GET"])
def api_bacnet_points():
    points = query_db(
        "SELECT p.id, p.name, p.object_type, p.last_value, p.unit, p.last_updated, "
        "d.name AS device_name "
        "FROM bacnet_points p LEFT JOIN bacnet_devices d ON p.device_id=d.id "
        "ORDER BY p.name"
    ) or []
    devices = query_db(
        "SELECT id, device_instance, name, ip_address, vendor, last_seen FROM bacnet_devices"
    ) or []
    return jsonify(
        {
            "points": [dict(r) for r in points],
            "devices": [dict(r) for r in devices],
        }
    )


@app.route("/api/bacnet/discover", methods=["POST"])
def api_bacnet_discover():
    """Trigger a BACnet network scan (async)."""
    def _scan():
        try:
            bacnet_cfg = load_config("bacnet.json")
            from bridge.bacnet_discovery import BACnetDiscovery
            import asyncio
            disc = BACnetDiscovery(
                interface=bacnet_cfg.get("interface", "eth0"),
                device_instance=bacnet_cfg.get("device_instance", 999),
                port=bacnet_cfg.get("port", 47808),
            )
            asyncio.run(disc.scan_devices())
        except Exception as exc:
            logger.error("BACnet scan error: %s", exc)

    threading.Thread(target=_scan, daemon=True).start()
    return jsonify({"ok": True, "message": "BACnet scan started"})


@app.route("/api/config/network", methods=["GET", "POST"])
def api_config_network():
    path = CONFIG_DIR / "network.json"
    if request.method == "POST":
        data = request.get_json(force=True) or {}
        try:
            with open(str(path), "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2)
            return jsonify({"ok": True})
        except Exception as exc:
            return jsonify({"ok": False, "error": str(exc)}), 500
    return jsonify(load_config("network.json"))


@app.route("/api/config/bacnet", methods=["GET", "POST"])
def api_config_bacnet():
    path = CONFIG_DIR / "bacnet.json"
    if request.method == "POST":
        data = request.get_json(force=True) or {}
        try:
            with open(str(path), "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2)
            return jsonify({"ok": True})
        except Exception as exc:
            return jsonify({"ok": False, "error": str(exc)}), 500
    return jsonify(load_config("bacnet.json"))


@app.route("/api/hmi/layout", methods=["GET", "POST"])
def api_hmi_layout():
    if request.method == "POST":
        data = request.get_json(force=True) or {}
        ok = execute_db(
            "INSERT OR REPLACE INTO network_config (key, value, updated_at) VALUES (?, ?, ?)",
            ("hmi_layout", json.dumps(data), datetime.utcnow().isoformat()),
        )
        return jsonify({"ok": ok})
    row = query_db(
        "SELECT value FROM network_config WHERE key='hmi_layout'", one=True
    )
    if row:
        try:
            return jsonify(json.loads(row["value"]))
        except Exception:
            pass
    return jsonify({"widgets": [], "pages": [{"name": "Page 1", "widgets": []}]})


@app.route("/api/hmi/deploy", methods=["POST"])
def api_hmi_deploy():
    data = request.get_json(force=True) or {}
    ok = execute_db(
        "INSERT OR REPLACE INTO network_config (key, value, updated_at) VALUES (?, ?, ?)",
        ("hmi_deployed_layout", json.dumps(data), datetime.utcnow().isoformat()),
    )
    if ok:
        socketio.emit("hmi_deployed", {"timestamp": datetime.utcnow().isoformat()})
    return jsonify({"ok": ok})

# ---------------------------------------------------------------------------
# Socket.IO — background polling loop
# ---------------------------------------------------------------------------

_poll_thread = None
_poll_running = False


def _poll_loop():
    """Background thread: poll DB every 5 s and emit point_update events."""
    global _poll_running
    interval = platform_cfg.get("poll_interval_seconds", 5)
    while _poll_running:
        try:
            points = query_db(
                "SELECT id, name, last_value, unit, last_updated FROM bacnet_points"
            ) or []
            for p in points:
                socketio.emit("point_update", dict(p))
        except Exception as exc:
            logger.debug("Poll loop error: %s", exc)
        time.sleep(interval)


@socketio.on("connect")
def on_connect():
    global _poll_thread, _poll_running
    logger.info("SocketIO client connected: %s", request.sid)
    if not _poll_running:
        _poll_running = True
        _poll_thread = threading.Thread(target=_poll_loop, daemon=True)
        _poll_thread.start()


@socketio.on("disconnect")
def on_disconnect():
    logger.info("SocketIO client disconnected: %s", request.sid)

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logger.info("Starting Minimal-PLC web server on 0.0.0.0:%d", WEB_PORT)
    socketio.run(app, host="0.0.0.0", port=WEB_PORT, debug=DEBUG)
