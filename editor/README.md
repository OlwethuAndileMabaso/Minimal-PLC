# Editor

This directory contains the tools you use on your **engineering PC** to design HMI screens and write PLC logic.

## Contents

| Directory | Tool | Purpose |
|-----------|------|---------|
| `hmi/designer/` | Freeboard | Drag-and-drop HMI screen designer — open `index.html` in your browser |
| `plc/openplc-editor/` | OpenPLC Editor | Write IEC 61131-3 ladder logic and deploy to the runtime |

## HMI Designer

Open `hmi/designer/index.html` directly in any modern browser — no server needed.

Design your dashboard, add widgets connected to your data sources, then save the board definition as a JSON file. Deploy that JSON to the runtime's Freeboard instance at `http://<target>:8080/hmi`.

## PLC Editor

Run the install script once to set up OpenPLC Editor:

```bash
cd plc/openplc-editor
bash install.sh
```

Then launch the editor, write your ladder logic program, and use the built-in deploy tool to push the compiled program to the OpenPLC Runtime running on the target machine.
