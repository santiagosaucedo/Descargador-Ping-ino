[app]
title = Descargador Pinguino
package.name = descargadorpinguino
package.domain = org.santiago
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,js,css,ico,webmanifest
source.include_patterns = motor-mobile-android/*, frontend/*
version = 1.0

# 🚨 MOTOR LIMPIO: Solo lo que Flask y yt-dlp necesitan para vivir
requirements = python3==3.11.11,hostpython3==3.11.11,flask,yt-dlp,openssl,libffi,sqlite3

# 🚨 BOOTSTRAP CORRECTO: Dejamos que Android maneje el navegador y los hilos
p4a.bootstrap = webview
p4a.port = 5000

icon.filename = frontend/android-chrome-512x512.png
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.ndk_api = 24
orientation = landscape
fullscreen = 1
android.manifest.application_attributes = android:usesCleartextTraffic="true"
android.archs = arm64-v8a
android.entrypoint = main.py