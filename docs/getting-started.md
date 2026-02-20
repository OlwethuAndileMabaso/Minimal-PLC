# Getting Started with Minimal-PLC

## Prerequisites

| Platform | Requirements |
|----------|-------------|
| Linux    | Python 3.8+, sudo access |
| Windows  | Python 3.8+, Administrator account |
| macOS    | Python 3.8+, Homebrew (auto-installed) |
| Android  | Android Studio, SDK 21+ |
| iOS      | Xcode 15+, macOS 13+ |

---

## 1. Clone the Repository

```bash
git clone https://github.com/OlwethuAndileMabaso/Minimal-PLC.git
cd Minimal-PLC
```

---

## 2. Install by Platform

### Linux (Debian/Ubuntu)

```bash
sudo bash scripts/install-linux.sh
```

This will:
- Install Python 3, SQLite, Chromium
- Create the `minimalplc` system user
- Install to `/opt/minimal-plc`
- Register and start the `minimal-plc` systemd service

**Verify:**
```bash
sudo systemctl status minimal-plc
curl http://localhost:8080/api/status
```

### Windows

Run **as Administrator**:
```bat
scripts\install-windows.bat
```

This will:
- Install Python dependencies
- Register the `MinimalPLC` Windows service via NSSM
- Open the browser to http://localhost:8080

### macOS

```bash
bash scripts/install-mac.sh
```

This will:
- Install Python via Homebrew
- Install to `~/MinimalPLC`
- Register a launchd agent that starts on login
- Open http://localhost:8080

### Manual (any platform)

```bash
python3 -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r runtime/requirements.txt
python runtime/webserver/server.py
```

---

## 3. First Login

Open **http://localhost:8080** and log in:

| Username | Password |
|----------|----------|
| admin    | admin    |

> ⚠️ **Change the default password immediately** via the Users page.

---

## 4. Configure BACnet

1. Go to **Network & Settings** (sidebar)
2. Under **BACnet Settings**, set:
   - **Interface** — your network interface (e.g. `eth0`, `en0`)
   - **Device Instance** — a unique number (e.g. `999`)
   - **BACnet Port** — default `47808`
3. Click **Save Settings**
4. Go to **BACnet Points** and click **Scan Network**

See [bacnet-guide.md](bacnet-guide.md) for more details.

---

## 5. Design an HMI Screen

1. Go to **HMI Designer** (sidebar)
2. Drag widgets from the left palette onto the canvas
3. Click a widget to edit its properties (title, data source, colours)
4. Click **Save** then **Deploy to Runtime**
5. Open **http://localhost:8080/hmi/runtime** to see the live screen

See [hmi-design-guide.md](hmi-design-guide.md) for more details.

---

## 6. Mobile Setup

### Android
1. Build from `mobile/android/` or install the APK
2. On first launch, enter `<your-server-ip>:8080`
3. The HMI runtime loads in fullscreen landscape mode

### iOS
1. Open `mobile/ios/MinimalPLC/` in Xcode
2. Set your development team and build to device
3. On first launch, enter `<your-server-ip>:8080`

---

## 7. Start / Stop

### Linux
```bash
sudo systemctl start minimal-plc
sudo systemctl stop  minimal-plc
```

### Windows
```bat
scripts\start.bat
scripts\stop.bat
```

### macOS / Manual
```bash
bash scripts/start.sh
bash scripts/stop.sh
```
