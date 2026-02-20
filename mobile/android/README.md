# Android App

A simple Android WebView app that loads the Minimal-PLC runtime interface.

## Prerequisites

- Android Studio (latest stable)
- Android SDK API 26+
- Java 17

## Build

1. Open `android/` in Android Studio
2. Edit `app/src/main/res/values/strings.xml` — set `runtime_url` to your PLC's IP address
3. Build → Generate Signed Bundle / APK

## Run

Install the APK on your Android device and launch **Minimal-PLC**.
