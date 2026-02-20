# HMI Design Guide

## Overview

The HMI designer is **Freeboard** — an open-source drag-and-drop dashboard builder.

- **Editor path:** `editor/hmi/designer/index.html` — open in any browser, no server needed
- **Runtime path:** `http://<target>:8080/hmi` — served to any browser by the Flask server

---

## Opening the Designer

1. Navigate to `editor/hmi/designer/`
2. Open `index.html` in Chrome, Firefox, or Edge
3. The Freeboard designer will load

---

## Adding a Data Source

1. Click **Add Datasource** in the top toolbar
2. Select **JSON** (or another type)
3. For live PLC data, use the **WebSocket** datasource:
   - URL: `ws://<target-ip>:8080/socket.io/?transport=websocket`
4. Name the datasource (e.g. `plc`)

---

## Adding Widgets

1. Click **Add Pane** to create a panel
2. Click the **+** button inside the pane to add a widget
3. Choose a widget type:
   - **Gauge** — for analog values (temperature, pressure)
   - **Indicator Light** — for binary on/off states
   - **Text** — for any value
   - **Sparkline** — for trending values
4. Bind the widget value to a datasource property

---

## Saving and Loading

- Click the **Save** icon to download the board as a JSON file
- Click the **Load** icon to load a previously saved board

---

## Deploying to the Runtime

Copy your saved board JSON to `runtime/webserver/hmi/` and rename it `dashboard.json`.
Freeboard will automatically load it when the HMI page opens.

---

## Customising Plugins

The `plugins/` directory contains Freeboard datasource and widget plugins. Add your own
`.js` plugin file and reference it from `index.html` to extend the designer.
