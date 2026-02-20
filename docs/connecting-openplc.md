# Connecting OpenPLC Runtime via Modbus TCP

This guide walks you through connecting OpenPLC Runtime to Minimal-PLC using Modbus TCP.

---

## 1. Installing OpenPLC Runtime

### Linux (Ubuntu/Debian):
```bash
git clone https://github.com/thiagoralves/OpenPLC_v3.git
cd OpenPLC_v3
./install.sh linux
```

### Windows:
Download the installer from [openplcproject.com](https://openplcproject.com) and run it.

Once installed, open the OpenPLC Runtime web interface at **http://localhost:8080**.

---

## 2. Connecting Minimal-PLC to OpenPLC via Modbus TCP

1. In OpenPLC Runtime, navigate to **Settings**
2. Enable **Modbus TCP Server** on port `502` (default)
3. Note the IP address of the machine running OpenPLC

In Minimal-PLC:
1. Navigate to **Devices**
2. Click **+ Add Device**
3. Fill in:
   - **Name**: `OpenPLC Runtime`
   - **Protocol**: `Modbus TCP`
   - **IP Address**: `192.168.1.10` (IP of OpenPLC machine)
   - **Port**: `502`
   - **Unit ID**: `1`
4. Click **Save**

---

## 3. Mapping OpenPLC Variables to Tags

OpenPLC uses a fixed Modbus memory map:

| OpenPLC Variable | Modbus Register | Modbus Type |
|---|---|---|
| `%QX0.0` | Coil 0 | Digital output |
| `%IX0.0` | Discrete Input 0 | Digital input |
| `%IW0` | Input Register 0 | Analog input |
| `%QW0` | Holding Register 0 | Analog output |

In Minimal-PLC:
1. Click on the OpenPLC device
2. Click **+ Add Tag**
3. Configure:
   - **Tag Name**: `Motor1Speed`
   - **Modbus Type**: `Holding Register`
   - **Register Address**: `0`
   - **Scale**: `0-32767 → 0-100%`
4. The tag is now available on the platform

---

## 4. Uploading PLC Programs

### Writing a Ladder Logic Program:
1. Install OpenPLC Editor from [openplcproject.com](https://openplcproject.com)
2. Create a new project (Ladder Diagram or Structured Text)
3. Define your I/O variables matching the Modbus map above
4. Compile the program

### Uploading to OpenPLC Runtime:
1. Open OpenPLC Runtime web interface (**http://localhost:8080**)
2. Navigate to **Programs**
3. Click **Upload Program** and select your `.st` file
4. Click **Start PLC** to begin execution

### Verifying in Minimal-PLC:
1. Navigate to **Trends**
2. Add your OpenPLC tags
3. Verify live values are updating
