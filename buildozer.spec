[app]
# (str) Título de tu aplicación en el menú del celular
title = Descargador Pinguino

# (str) Nombre del paquete (identificador único, usa letras minúsculas sin espacios)
package.name = descargadorpinguino

# (str) Dominio de organización para el ID interno
package.domain = org.santiago

# (str) Directorio donde se encuentra el código fuente de Android
source.dir = motor-mobile-android

# (list) Extensiones de archivos que se van a incluir en el APK
source.include_exts = py,png,jpg,kv,atlas,html,js,css,ico,webmanifest

# (str) Versión de tu aplicación
version = 1.0

# (list) Requerimientos de librerías de Python necesarios para correr el servidor
requirements = python3,flask,yt-dlp

# (str) Ícono para el celular (Usamos el de alta definición que está adentro de frontend)
icon.filename = %(source.dir)s/../frontend/android-chrome-512x512.png

# (list) Permisos de Android necesarios (Descarga de Internet y Guardado en Almacenamiento)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (str) Supported orientation (one of landscape, portrait or all)
orientation = landscape

# (bool) Indicar si la aplicación corre a pantalla completa (oculta barras del sistema)
fullscreen = 1

# (list) Arquitecturas de procesadores de celular a compilar (Arm64 es el estándar actual)
android.archs = arm64-v8a

# (str) Indicarle a Buildozer que empaquete un WebView para renderizar tu Canvas HTML5
android.entrypoint = main.py