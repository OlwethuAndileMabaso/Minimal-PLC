# iOS App

A simple iOS WKWebView app that loads the Minimal-PLC runtime interface.

## Prerequisites

- Xcode 15+
- iOS 15+ target
- macOS development machine

## Build

1. Open `ios/MinimalPLC.xcodeproj` in Xcode (create a new project, add the Swift files)
2. Edit `ViewController.swift` — set `runtimeURL` to your PLC's IP address
3. Build and run on a device or simulator

## Deploy

Archive the app in Xcode and distribute via TestFlight or direct install.
