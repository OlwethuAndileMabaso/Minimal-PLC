# Connecting EasyIO Devices via BACnet/IP

This guide walks you through connecting EasyIO field controllers (FT-04, FW-14, etc.) to Minimal-PLC using BACnet/IP.

---

## 1. EasyIO BACnet/IP Setup

Before connecting, ensure your EasyIO controller is configured for BACnet/IP:

1. Access the EasyIO web interface (default: `http://192.168.1.50`)
2. Navigate to **Settings → BACnet**
3. Set the **Device Instance** (unique number, e.g. `1001`)
4. Set the **IP address** to match your network subnet
5. Enable **BACnet/IP** and set **UDP port** to `47808` (default)
6. Save and reboot the controller

---

## 2. Adding EasyIO as a Device in Minimal-PLC

1. Start Minimal-PLC (`npm run dev`)
2. Open the browser at **http://localhost:4200**
3. Navigate to **Devices** in the sidebar
4. Click **+ Add Device**
5. Fill in the device form:
   - **Name**: `EasyIO FT-04`
   - **Protocol**: `BACnet/IP`
   - **IP Address**: `192.168.1.50` (your controller IP)
   - **Port**: `47808`
   - **Device Instance**: `1001`
6. Click **Save** — the device will appear in the list with a green status dot

---

## 3. Mapping BACnet Points to Tags

1. Click on the device name to open its tag list
2. Click **Discover Points** — Minimal-PLC will scan the BACnet device
3. Available points (Analog Input, Binary Input, etc.) will appear
4. Select the points you want to monitor
5. Click **Map to Tags** — each point becomes a named tag
6. Tags are now available throughout the platform

Example points:
| BACnet Object | Tag Name | Description |
|---|---|---|
| AI:1 | `Zone3Temp` | Zone 3 Temperature |
| AI:2 | `SupplyAirTemp` | Supply Air Temperature |
| BO:1 | `Fan1Command` | Fan 1 On/Off command |

---

## 4. Binding Tags to HMI Widgets

1. Navigate to **HMI Designer**
2. Drag a **Gauge** widget onto the canvas
3. Click the widget to select it
4. In the **Properties** panel, find the **Tag** field
5. Select `Zone3Temp` from the dropdown
6. The gauge will now display live data from the BACnet controller

---

## 5. Testing Live Data

1. Navigate to **Trends**
2. Click **+ Add Tag** and select `Zone3Temp`
3. Select time range **1H**
4. You should see live data being plotted
5. If no data appears, check:
   - Device is reachable: `ping 192.168.1.50`
   - BACnet port is open: UDP 47808
   - Device instance is correct
