import os
import binascii
import subprocess
from flask import Flask, request, jsonify, send_from_directory

RUTA_BASE_MOBILE = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROYECTO = os.path.dirname(RUTA_BASE_MOBILE)
CARPETA_FRONTEND = os.path.join(RAIZ_PROYECTO, "frontend")
ES_ANDROID = 'ANDROID_ARGUMENT' in os.environ

app = Flask(__name__, static_folder=CARPETA_FRONTEND, static_url_path='')

def obtener_ruta_descargas():
    """Calcula la ruta segura dependiendo del sistema operativo."""
    if ES_ANDROID:
        # Usamos la carpeta pública de descargas de Android
        ruta = '/storage/emulated/0/Download'
    else:
        ruta = os.path.join(os.path.expanduser("~"), "Downloads")
    
    os.makedirs(ruta, exist_ok=True)
    return ruta

@app.route('/')
def servir_interfaz():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/descargar_video', methods=['POST'])
def api_descargar_video():
    data = request.json or {}
    url_video = data.get('url', '')

    if not url_video or ("youtube.com" not in url_video and "youtu.be" not in url_video):
        return jsonify({"status": "error", "message": "Enlace inválido."}), 400

    try:
        ruta_final = obtener_ruta_descargas()
    except Exception as e:
        return jsonify({"status": "error", "message": f"Sin permisos de escritura: {e}"}), 500

    url_limpia = url_video.strip().split()[0]

    from yt_dlp import YoutubeDL
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": os.path.join(ruta_final, "%(title)s.%(ext)s"),
        "quiet": True,
        "restrictfilenames": True,
    }

    if not ES_ANDROID:
        FFMPEG_PATH = os.path.join(RAIZ_PROYECTO, "motor-desktop-pc", "bin", "ffmpeg.exe")
        ydl_opts["ffmpeg_location"] = os.path.dirname(FFMPEG_PATH)

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_limpia])
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/convertir_bytes', methods=['POST'])
def api_convertir_bytes():
    # Mantenemos tu lógica intacta, inyectando la ruta de forma segura
    data = request.json or {}
    nombre_archivo = data.get('nombre', '')
    datos_hex = data.get('hex', '')

    if not datos_hex or len(datos_hex) % 2 != 0:
        return jsonify({"status": "error", "message": "Flujo corrupto."}), 400

    try:
        ruta_final = obtener_ruta_descargas()
    except Exception as e:
        return jsonify({"status": "error", "message": f"Sin permisos de escritura: {e}"}), 500

    try:
        nombre_seguro = os.path.basename(nombre_archivo)
        nombre_puro = os.path.splitext(nombre_seguro)[0]
        archivo_bytes = binascii.unhexlify(datos_hex)

        ruta_temporal = os.path.join(ruta_final, f"temp_{nombre_seguro}")
        ruta_salida_mp3 = os.path.join(ruta_final, f"{nombre_puro}.mp3")

        with open(ruta_temporal, "wb") as f:
            f.write(archivo_bytes)

        if ES_ANDROID:
            executable_ffmpeg = "ffmpeg"
        else:
            executable_ffmpeg = os.path.join(RAIZ_PROYECTO, "motor-desktop-pc", "bin", "ffmpeg.exe")

        comando = [executable_ffmpeg, "-i", ruta_temporal, "-vn", "-q:a", "0", "-y", ruta_salida_mp3]
        subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if os.path.exists(ruta_temporal): os.remove(ruta_temporal)
        return jsonify({"status": "ok"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)