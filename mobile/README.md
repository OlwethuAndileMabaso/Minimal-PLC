# Mobile — Android & iOS HMI Viewers

Both mobile apps load the Minimal-PLC HMI runtime (`/hmi/runtime`) in a fullscreen WebView,
providing a native kiosk experience on tablets and phones.

## Android

**Requirements:** Android Studio, SDK 21+

```bash
cd mobile/android
./gradlew assembleDebug
```

Install with:
```bash
adb install app/build/outputs/apk/debug/app-debug.apk
```

## iOS

**Requirements:** Xcode 15+, macOS 13+

Open `mobile/ios/MinimalPLC/` in Xcode, set your development team,
and run on device or simulator.

## First Launch

On first launch both apps display a dialog asking for the server IP and port
(default: `192.168.1.100:8080`). This is saved to preferences and can be
changed by long-pressing on the loading screen.
