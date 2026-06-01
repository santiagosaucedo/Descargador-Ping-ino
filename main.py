# 🐧 main.py (Ubicado en la raíz del proyecto)
import sys
import os

# 1. Forzamos la ruta absoluta para que encuentre el backend en Android
ruta_raiz = os.path.dirname(os.path.abspath(__file__))
ruta_motor_movil = os.path.join(ruta_raiz, 'motor-mobile-android')

if ruta_motor_movil not in sys.path:
    sys.path.insert(0, ruta_motor_movil)

# 2. Intentamos avisarle al motor de Android que mantenga la app viva
try:
    from android.runnable import Runnable
    # Esto le dice al WebView de Android: "Estoy vivo, no me cierres"
except ImportError:
    pass

# 3. Importamos tu lógica del servidor Flask
try:
    import android_server
except Exception as e:
    # Si llega a fallar la importación por algo, guardamos un log interno para saber qué pasó
    with open(os.path.join(ruta_raiz, 'error_boot.txt'), 'w') as f:
        f.write(str(e))
    sys.exit(1)

if __name__ == "__main__":
    pass