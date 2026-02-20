# Getting Started

This guide walks you through setting up Minimal-PLC from scratch.

## What You Need

| Item | Details |
|------|---------|
| Engineering PC | Any OS — Windows, macOS, or Linux |
| Target machine | Linux (Raspberry Pi, Ubuntu PC) or Windows machine |
| Network | Both machines on the same LAN |

---

## Step 1 — Install the Runtime on the Target Machine

Clone the repository on the **target machine**:

```bash
git clone https://github.com/OlwethuAndileMabaso/Minimal-PLC.git
cd Minimal-PLC
```

### Linux
```bash
bash scripts/install-linux.sh
```

### Windows
```bat
scripts\install-windows.bat
```

### macOS
```bash
bash scripts/install-mac.sh
```

---

## Step 2 — Configure

Edit the JSON files in `config/` before starting:

- **`config/platform.json`** — Change the port if needed (default: 8080)
- **`config/bacnet.json`** — Add your BACnet device points
- **`config/network.json`** — Network interface settings

---

## Step 3 — Start the Runtime

```bash
cd runtime
bash start.sh       # Linux/macOS
start.bat           # Windows
```

Open **http://\<target-ip\>:8080** in any browser on your LAN.

---

## Step 4 — Design the HMI

On your **engineering PC**, open `editor/hmi/designer/index.html` in a browser.

Drag and drop widgets to build your dashboard. Connect data sources to the runtime WebSocket endpoint (`ws://<target>:8080`). Save the board as JSON.

---

## Step 5 — Write PLC Logic

```bash
cd editor/plc/openplc-editor
bash install.sh
```

Launch the OpenPLC Editor, write your IEC 61131-3 program, and deploy it to the runtime.

---

## Next Steps

- [Architecture Overview](architecture.md)
- [BACnet Integration Guide](bacnet-guide.md)
- [HMI Design Guide](hmi-design-guide.md)
