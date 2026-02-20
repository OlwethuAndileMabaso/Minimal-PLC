# Editor — OpenPLC Editor Integration

The `editor/` directory is the integration point for the OpenPLC Editor,
which provides a full IEC 61131-3 graphical programming environment
(Ladder Diagram, Function Block Diagram, Structured Text, etc.).

## Source

**OpenPLC Editor** — [thiagoralves/OpenPLC_Editor](https://github.com/thiagoralves/OpenPLC_Editor) (GPL-2.0)

## Installation

```bash
bash editor/install.sh
```

This clones the OpenPLC Editor repository and installs its dependencies.

## Usage

After installation, launch the editor with:

```bash
python OpenPLC_Editor/openplc_editor.py
```

Write your PLC program, compile it, and upload the generated `.st` file
via the **Programs** page in the Minimal-PLC web interface.
