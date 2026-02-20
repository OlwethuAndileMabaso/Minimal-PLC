# iOS HMI App

Fullscreen WKWebView application for the Minimal-PLC HMI runtime.

## Building

Open the `MinimalPLC/` directory in Xcode 15+. Set your development team
under Signing & Capabilities, then build and run on a device or simulator.

## Configuration

On first launch the app shows a dialog requesting the server address
(default: `192.168.1.100:8080`). This is stored in UserDefaults.
