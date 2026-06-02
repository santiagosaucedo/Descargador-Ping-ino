# 🐧 main.py (Ubicado en la raíz del proyecto)
import sys
import os

# 1. Inyectamos la ruta del motor móvil para que encuentre tu servidor
ruta_raiz = os.path.dirname(os.path.abspath(__file__))
ruta_motor_movil = os.path.join(ruta_raiz, 'motor-mobile-android')
if ruta_motor_movil not in sys.path:
    sys.path.insert(0, ruta_motor_movil)

# 2. CONFIGURACIÓN CRÍTICA DE RUTAS PARA ANDROID
# Detectamos si corre en el celular para inyectar la ruta donde yt-dlp sí puede escribir
if 'ANDROID_ARGUMENT' in os.environ:
    from android.storage import app_storage_dir
    ruta_descargas = os.path.join(app_storage_dir(), 'downloads')
else:
    # Ruta por defecto si estás probando local en tu PC
    ruta_descargas = os.path.join(ruta_raiz, 'downloads')

os.makedirs(ruta_descargas, exist_ok=True)

# Seteamos la ruta en el entorno del sistema para que android_server.py la pueda leer
os.environ['RUTA_DESCARGAS_PINGUINO'] = ruta_descargas

# 3. Importamos y arrancamos tu servidor Flask
import android_server

if __name__ == "__main__":
    # Arrancamos Flask en el puerto local y el WebView se acopla solo
    android_server.app.run(host='127.0.0.1', port=5000, debug=False)