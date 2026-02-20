# Android HMI App

Fullscreen WebView application for the Minimal-PLC HMI runtime.

## Building

```bash
cd mobile/android
./gradlew assembleDebug
```

The APK is output to `app/build/outputs/apk/debug/app-debug.apk`.

## Configuration

On first launch the app shows a dialog requesting the server address
(default: `192.168.1.100:8080`). This is stored in SharedPreferences.
