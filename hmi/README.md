# HMI — Designer and Runtime

| Directory | Description |
|-----------|-------------|
| `designer/` | Drag-and-drop HMI screen designer (served at `/hmi/designer/`) |
| `runtime/`  | Fullscreen kiosk HMI runtime for operators (served at `/hmi/runtime`) |

## Designer Features
- Drag widgets from the left palette onto the canvas
- Click a widget to edit its properties in the right panel
- **Save** — persists layout to localStorage
- **Deploy** — pushes layout to the server via `POST /api/hmi/deploy`
- **Preview** — opens the runtime in a new tab

## Runtime Features
- Loads deployed layout from `GET /api/hmi/layout`
- Real-time value updates via Socket.IO `point_update` events
- Alarm banner on `alarm` events
- Touch-friendly (44 px minimum targets)
- Auto-reconnects every 5 seconds on disconnect
