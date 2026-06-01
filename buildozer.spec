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

# (list) Application requirements (Agregado pyjnius al final para el puente gráfico)
requirements = python3==3.11.11,hostpython3==3.11.11,flask,yt-dlp,pyjnius

# (str) Ícono para el celular
icon.filename = frontend/android-chrome-512x512.png

# (list) Permisos de Android necesarios (Dejamos solo INTERNET para el testeo inicial limpio)
android.permissions = INTERNET

# (int) Target Android API (Versión estable apuntando a Android 13)
android.api = 33

# (int) Minimum API required (Android 7.0 en adelante)
android.minapi = 24

# (int) Android NDK API to use
android.ndk_api = 24

# (str) Orientación fija en horizontal
orientation = landscape

# (bool) Pantalla completa sin barras de estado
fullscreen = 1

# (list) Arquitectura estándar moderna
android.archs = arm64-v8a

# (str) Punto de entrada oficial
android.entrypoint = main.py