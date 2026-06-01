import os
import binascii
import subprocess
from flask import Flask, request, jsonify, send_from_directory

# --- MANEJO DINÁMICO DE RUTAS BASADO EN TU ÁRBOL DE DIRECTORIOS ---
RUTA_BASE_MOBILE = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROYECTO = os.path.dirname(RUTA_BASE_MOBILE)
CARPETA_FRONTEND = os.path.join(RAIZ_PROYECTO, "frontend")
FFMPEG_PATH = os.path.join(RAIZ_PROYECTO, "motor-desktop-pc", "bin")

executable_ffmpeg = os.path.join(FFMPEG_PATH, "ffmpeg.exe")
RUTA_DESCARGAS_USUARIO = os.path.join(os.path.expanduser("~"), "Downloads")

# Inicializamos Flask apuntando exactamente a la carpeta externa /frontend
app = Flask(__name__, static_folder=CARPETA_FRONTEND, static_url_path='')


@app.route('/')
def servir_interfaz():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/descargar_video', methods=['POST'])
def api_descargar_video():
    data = request.json or {}
    url_video = data.get('url', '')

    if not url_video or ("youtube.com" not in url_video and "youtu.be" not in url_video):
        return jsonify({"status": "error", "message": "Enlace inválido."}), 400

    url_limpia = url_video.strip().split()[0]

    from yt_dlp import YoutubeDL
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "ffmpeg_location": FFMPEG_PATH,
        "outtmpl": os.path.join(RUTA_DESCARGAS_USUARIO, "%(title)s.%(ext)s"),
        "quiet": True,
        "restrictfilenames": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_limpia])
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/convertir_bytes', methods=['POST'])
def api_convertir_bytes():
    data = request.json or {}
    nombre_archivo = data.get('nombre', '')
    datos_hex = data.get('hex', '')

    if not datos_hex or len(datos_hex) % 2 != 0:
        return jsonify({"status": "error", "message": "Flujo de bytes corrupto."}), 400

    try:
        nombre_seguro = os.path.basename(nombre_archivo)
        nombre_puro = os.path.splitext(nombre_seguro)[0]

        archivo_bytes = binascii.unhexlify(datos_hex)

        ruta_temporal_video = os.path.join(RUTA_DESCARGAS_USUARIO, f"temp_mobile_{nombre_seguro}")
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

        return jsonify({"status": "ok"})

    except Exception as e:
        if 'ruta_temporal_video' in locals() and os.path.exists(ruta_temporal_video):
            os.remove(ruta_temporal_video)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    print("Servidor móvil simulado listo en : http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False)