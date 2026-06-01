# 🐧 main.py (Puesto en la raíz del proyecto)
import sys
import os

# Le decimos a Python que busque adentro de la carpeta del motor móvil
sys.path.append(os.path.join(os.path.dirname(__file__), 'motor-mobile-android'))

# Importamos y ejecutamos tu servidor de Flask
import android_server

if __name__ == "__main__":
    pass