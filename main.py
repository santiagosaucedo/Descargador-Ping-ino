# 🐧 main.py (Punto de entrada minimalista para WebView)
import sys
import os

# 1. Acoplamos las rutas de tu arquitectura
ruta_raiz = os.path.dirname(os.path.abspath(__file__))
ruta_motor_movil = os.path.join(ruta_raiz, 'motor-mobile-android')
if ruta_motor_movil not in sys.path:
    sys.path.insert(0, ruta_motor_movil)

# 2. Arrancamos Flask de forma directa
if __name__ == "__main__":
    try:
        import android_server
        # El motor 'webview' de Android automáticamente captura este puerto y lo muestra en pantalla
        android_server.app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Error fatal levantando el servidor: {e}")