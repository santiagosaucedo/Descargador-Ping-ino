import os
import sys
import subprocess
import eel

# --- DETECTAR SI CORRE COMO SCRIPT O COMO COMPILADO EXE ---
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # Entorno de Ejecución (.EXE): PyInstaller descomprime todo en la carpeta temporal _MEIPASS
    RUTA_FRONTEND = os.path.join(sys._MEIPASS, "frontend")
else:
    # Entorno de Desarrollo (VS Code): Buscamos la carpeta /frontend subiendo un nivel
    RUTA_BASE_PROYECTO = os.path.dirname(os.path.abspath(__file__))
    RAIZ_PROYECTO = os.path.dirname(RUTA_BASE_PROYECTO)
    RUTA_FRONTEND = os.path.join(RAIZ_PROYECTO, "frontend")

# Inicializamos Eel apuntando a la ruta dinámica resuelta para evitar el Error 404
eel.init(RUTA_FRONTEND)

# --- RECONFIGURACIÓN DE RUTAS DE BINARIOS PORTABLES ---
if getattr(sys, 'frozen', False):
    # En el ejecutable compilado, el binario vive dentro del paquete extraído
    FFMPEG_PATH = os.path.join(sys._MEIPASS, "motor-desktop-pc", "bin")
else:
    # En desarrollo local de PC, está en tu subcarpeta bin habitual
    RUTA_BASE_PROYECTO = os.path.dirname(os.path.abspath(__file__))
    FFMPEG_PATH = os.path.join(RUTA_BASE_PROYECTO, "bin")

executable_ffmpeg = os.path.join(FFMPEG_PATH, "ffmpeg.exe")
RUTA_DESCARGAS_USUARIO = os.path.join(os.path.expanduser("~"), "Downloads")


@eel.expose
def backend_descargar_video(url_video):
    """Descarga de video bloqueando inyecciones de parámetros en yt-dlp."""
    if not isinstance(url_video, str) or ("youtube.com" not in url_video and "youtu.be" not in url_video):
        return {"status": "error", "message": "Enlace no válido."}

    # Limpieza de caracteres de escape que puedan alterar la consola
    url_limpia = url_video.strip().split()[0]

    from yt_dlp import YoutubeDL
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "ffmpeg_location": FFMPEG_PATH,
        "outtmpl": os.path.join(RUTA_DESCARGAS_USUARIO, "%(title)s.%(ext)s"),
        "quiet": True,
        "restrictfilenames": True, # Forzar nombres de archivos seguros frente a exploits lógicos
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_limpia])
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@eel.expose
def backend_convertir_bytes_a_mp3(nombre_archivo, datos_hex):
    """Procesa flujos hexadecimales puros controlando desbordamientos de memoria."""
    if not isinstance(datos_hex, str) or len(datos_hex) % 2 != 0:
        return {"status": "error", "message": "Datos corruptos."}

    try:
        nombre_seguro = os.path.basename(nombre_archivo)
        nombre_puro = os.path.splitext(nombre_seguro)[0]
        
        # Conversión segura de hex a bytes puros en memoria
        archivo_bytes = bytes.fromhex(datos_hex)

        ruta_temporal_video = os.path.join(RUTA_DESCARGAS_USUARIO, f"temp_{nombre_seguro}")
        ruta_salida_mp3 = os.path.join(RUTA_DESCARGAS_USUARIO, f"{nombre_puro}.mp3")

        with open(ruta_temporal_video, "wb") as f:
            f.write(archivo_bytes)

        comando = [
            executable_ffmpeg,
            "-i", ruta_temporal_video,
            "-vn",
            "-q:a", "0",
            "-y",
            ruta_salida_mp3
        ]

        subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if os.path.exists(ruta_temporal_video):
            os.remove(ruta_temporal_video)

        return {"status": "ok"}

    except Exception as e:
        if 'ruta_temporal_video' in locals() and os.path.exists(ruta_temporal_video):
            os.remove(ruta_temporal_video)
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    print("Controladores listos")
    eel.start("index.html", size=(870, 560))