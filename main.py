# 🐧 main.py (Ubicado en la raíz del proyecto)
import sys
import os

# Inyectamos la ruta del motor móvil para que encuentre tu servidor
ruta_raiz = os.path.dirname(os.path.abspath(__file__))
ruta_motor_movil = os.path.join(ruta_raiz, 'motor-mobile-android')
if ruta_motor_movil not in sys.path:
    sys.path.insert(0, ruta_motor_movil)

# Importamos tu servidor Flask
import android_server

if __name__ == "__main__":
    # Arrancamos Flask en el puerto local y el WebView de Android se acopla solo
    android_server.app.run(host='127.0.0.1', port=5000, debug=False)