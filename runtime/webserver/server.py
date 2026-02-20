"""
Minimal-PLC Runtime Web Server
Flask + SocketIO server serving the HMI and management dashboard on port 8080.
"""

import json
import os

from flask import Flask, redirect, render_template, send_from_directory, url_for
from flask_socketio import SocketIO

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "..", "config")


def load_config(filename: str) -> dict:
    """Load a JSON config file from the config directory."""
    path = os.path.join(CONFIG_DIR, filename)
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "minimal-plc-secret")
socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

platform_config = load_config("platform.json")
network_config = load_config("network.json")
bacnet_config = load_config("bacnet.json")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.route("/")
def index():
    """Redirect root to the dashboard."""
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        platform=platform_config,
        active="dashboard",
    )


@app.route("/bacnet")
def bacnet():
    return render_template(
        "bacnet.html",
        bacnet=bacnet_config,
        active="bacnet",
    )


@app.route("/network")
def network():
    return render_template(
        "network.html",
        network=network_config,
        active="network",
    )


@app.route("/settings")
def settings():
    return render_template(
        "settings.html",
        platform=platform_config,
        active="settings",
    )


@app.route("/hmi/")
@app.route("/hmi")
def hmi():
    """Serve the Freeboard HMI index page."""
    hmi_dir = os.path.join(BASE_DIR, "hmi")
    return send_from_directory(hmi_dir, "index.html")


@app.route("/hmi/<path:filename>")
def hmi_static(filename):
    """Serve static Freeboard HMI assets."""
    hmi_dir = os.path.join(BASE_DIR, "hmi")
    return send_from_directory(hmi_dir, filename)


# ---------------------------------------------------------------------------
# SocketIO events
# ---------------------------------------------------------------------------


@socketio.on("connect")
def on_connect():
    pass


@socketio.on("disconnect")
def on_disconnect():
    pass


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(platform_config.get("port", 8080))
    host = platform_config.get("host", "0.0.0.0")
    debug = platform_config.get("debug", False)
    socketio.run(app, host=host, port=port, debug=debug)
