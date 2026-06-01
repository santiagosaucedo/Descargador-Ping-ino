# 🐧 main.py (Ubicado en la raíz del proyecto)
import sys
import os

# 1. Obtenemos la ruta absoluta de la carpeta donde está parado este main.py
ruta_raiz = os.path.dirname(os.path.abspath(__file__))

# 2. Construimos la ruta exacta hacia la carpeta del motor móvil
ruta_motor_movil = os.path.join(ruta_raiz, 'motor-mobile-android')

# 3. Le inyectamos esa ruta a Python para que encuentre a android_server
if ruta_motor_movil not in sys.path:
    sys.path.insert(0, ruta_motor_movil)

# 4. Ahora sí, importamos tu servidor de Flask sin errores de resolución
import android_server

if __name__ == "__main__":
    # Dejamos que el bloque interno de android_server maneje el inicio
    pass