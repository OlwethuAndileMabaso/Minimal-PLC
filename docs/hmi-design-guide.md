# HMI Design Guide

## Opening the Designer

Navigate to **HMI Designer** in the sidebar, or go directly to `/hmi`.
The designer is embedded in an iframe at the bottom of the page.

---

## Widget Types

| Widget | Icon | Description |
|--------|------|-------------|
| Gauge  | 📊  | Circular gauge showing a numeric value |
| Value  | 🔢  | Large numeric display |
| Chart  | 📈  | Line chart (coming soon) |
| Status Light | 🔴 | Green/red indicator |
| Button | 🔘  | Clickable control |
| Label  | 🏷️  | Static text |
| Alarms | 🚨  | Live alarm list |

---

## Adding Widgets

1. **Drag** a widget from the left palette
2. **Drop** it onto the dark canvas
3. The widget appears at the drop position

---

## Data Binding

Click a widget to select it. In the **Properties** panel on the right:

| Property | Description |
|----------|-------------|
| Title | Display label |
| Data Source | BACnet point name (must match `bacnet_points.name` in the DB) |
| Min / Max | Value range for gauges |
| Color | Border and value text colour |
| Width / Height | Widget dimensions in pixels |

When the HMI runtime is open and a Socket.IO `point_update` event arrives
with `name` matching the **Data Source**, the widget value updates live.

---

## Multiple Pages

- Click **＋** in the page tab bar at the bottom to add a page
- Click a page tab to switch to it
- Each page has its own widget layout

---

## Saving

Click **Save** in the toolbar. The layout is saved to `localStorage` in the browser.

---

## Deploying

Click **Deploy to Runtime**. This sends the current layout as JSON to
`POST /api/hmi/deploy`, which stores it in the database.

All connected HMI runtime instances reload the layout automatically via
the `hmi_deployed` Socket.IO event.

---

## Viewing the Runtime

- Click **Open Runtime** button (or navigate to `/hmi/runtime`)
- For full-screen kiosk: open `/hmi/runtime` in a browser, press F11
- On Android/iOS: use the Minimal-PLC mobile app

---

## Tips

- Use the **Properties** panel Color picker to give different widgets distinct colours
- Name your Data Sources to match your BACnet point names exactly (case-sensitive)
- Use **Page 1** for operator overview and add pages for specific equipment
- The runtime auto-reconnects to the server if the connection is lost
