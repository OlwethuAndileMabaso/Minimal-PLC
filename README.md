# Minimal-PLC

> Open-source Industrial HMI + PLC Platform

**Platform Support:** Linux ✅ Windows ✅ macOS ✅ Android ✅ iOS ✅ Any Browser ✅

Minimal-PLC is a complete open-source platform for building industrial control systems. It consists of two clear parts: an **Editor** you use on your engineering PC to design screens and write PLC logic, and a **Runtime** that runs 24/7 on the target machine.

---

## Architecture

```
EDITOR (engineer uses this on their PC)
├── hmi/designer/     ← Freeboard — drag & drop HMI screen designer
└── plc/              ← OpenPLC Editor — write ladder logic

        ↓ Deploy

RUNTIME (runs 24/7 on target machine - Linux or Windows)
├── webserver/        ← Flask server at :8080, serves Freeboard HMI to any browser
├── plc/              ← OpenPLC Runtime — executes PLC logic
├── bacnet/           ← Reads live values from BACnet devices on network
└── database/         ← SQLite — stores history, alarms, config
```

---

## Quick Start

### Step 1 — Install the Runtime (on your target machine)

**Linux:**
```bash
git clone https://github.com/OlwethuAndileMabaso/Minimal-PLC.git
cd Minimal-PLC
bash scripts/install-linux.sh
```

**Windows:**
```bat
git clone https://github.com/OlwethuAndileMabaso/Minimal-PLC.git
cd Minimal-PLC
scripts\install-windows.bat
```

**macOS:**
```bash
git clone https://github.com/OlwethuAndileMabaso/Minimal-PLC.git
cd Minimal-PLC
bash scripts/install-mac.sh
```

### Step 2 — Start the Runtime

**Linux/macOS:**
```bash
cd runtime
bash start.sh
```

**Windows:**
```bat
cd runtime
start.bat
```

Open your browser at **http://localhost:8080**

### Step 3 — Design your HMI (on your engineering PC)

Open `editor/hmi/designer/index.html` in your browser to use the Freeboard drag-and-drop designer.

### Step 4 — Write PLC Logic

Use the OpenPLC Editor in `editor/plc/openplc-editor/` — run `install.sh` to set it up, then write ladder logic and deploy to the runtime.

---

## Credits

- **OpenPLC Runtime** — [thiagoralves/OpenPLC_v3](https://github.com/thiagoralves/OpenPLC_v3) (GPL-3.0)
- **OpenPLC Editor** — [thiagoralves/OpenPLC_Editor](https://github.com/thiagoralves/OpenPLC_Editor) (GPL-2.0)
- **Freeboard HMI** — [Freeboard/freeboard](https://github.com/Freeboard/freeboard) (MIT)

---

## License

MIT — see [LICENSE](LICENSE)