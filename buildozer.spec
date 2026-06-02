[app]

# (str) Título de tu aplicación en el menú del celular
title = Descargador Pinguino

# (str) Nombre del paquete (identificador único, usa letras minúsculas sin espacios)
package.name = descargadorpinguino

# (str) Dominio de organización para el ID interno
package.domain = org.santiago

# (str) Directorio raíz (Leemos desde la raíz para unificar frontend y backend)
source.dir = .

# (list) Extensiones de archivos válidas
source.include_exts = py,png,jpg,kv,atlas,html,js,css,ico,webmanifest

# (list) FILTRO CRÍTICO: Incluimos solo las carpetas de la app y dejamos afuera .venv y .git
source.include_patterns = motor-mobile-android/*, frontend/*

# (str) Versión de tu aplicación
version = 1.0

# (list) Application requirements
requirements = python3==3.11.11,hostpython3==3.11.11,flask,yt-dlp,openssl,libffi,sqlite3,kivy,pyjnius

# 🚨 El bootstrap TIENE que ser sdl2 para poder usar el decorador @run_on_ui_thread
p4a.bootstrap = sdl2

# (str) Ícono para el celular
icon.filename = frontend/android-chrome-512x512.png

# (list) Permisos de Android necesarios
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API (Versión de Android 13 estable)
android.api = 33

# (int) Minimum API required (Android 7.0 en adelante)
android.minapi = 24

# (int) Android NDK API to use
android.ndk_api = 24

# (str) Orientación fija en horizontal
orientation = landscape

# (bool) Pantalla completa sin barras de estado
fullscreen = 1

# (bool) Permitir tráfico HTTP sin cifrar (Clave para que Android 9+ lea el localhost)
android.manifest.application_attributes = android:usesCleartextTraffic="true"

# (list) Arquitectura estándar moderna
android.archs = arm64-v8a

# (str) Punto de entrada oficial (Llama al main.py limpio que reescribimos)
android.entrypoint = main.py