# 🐧 main.py (Ubicado en la raíz del proyecto)
import sys
import os
import threading
import time

# 1. Configurar rutas para encontrar el backend
ruta_raiz = os.path.dirname(os.path.abspath(__file__))
ruta_motor_movil = os.path.join(ruta_raiz, 'motor-mobile-android')
if ruta_motor_movil not in sys.path:
    sys.path.insert(0, ruta_motor_movil)

# 2. Función para correr Flask en un hilo separado
def iniciar_servidor_flask():
    try:
        import android_server
    except Exception as e:
        with open(os.path.join(ruta_raiz, 'error_flask.txt'), 'w') as f:
            f.write(str(e))

# Lanzamos Flask en segundo plano para que no bloquee el arranque de Android
hilo_flask = threading.Thread(target=iniciar_servidor_flask)
hilo_flask.daemon = True
hilo_flask.start()

# Esperamos un toque a que el servidor Flask levante el puerto
time.sleep(1.5)

# 3. LEVANTAR EL WEBVIEW NATIVO DE ANDROID
# Esto evita que la app se cierre sola porque le da una ventana real al sistema
try:
    from jnius import autoclass
    from android.runnable import Runnable

    # Enganches nativos con las clases de Java de Android
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')

    class CrearWebView(Runnable):
        def run(self):
            activity = PythonActivity.mActivity
            webview = WebView(activity)
            # Permitir Javascript para que corra tu Canvas del Pingüino
            webview.getSettings().setJavaScriptEnabled(True)
            webview.setWebViewClient(WebViewClient())
            # Cargamos tu servidor local de Flask
            webview.loadUrl('http://127.0.0.1:5000')
            activity.setContentView(webview)

    # Ejecutamos la ventana en el hilo principal de la interfaz de Android
    CrearWebView()()

    # Mantenemos el script principal en un bucle infinito para que no muera la app
    while True:
        time.sleep(1)

except ImportError:
    # Si estás probando en PC local, esto evita que falle por no tener las librerías de Android
    print("Corriendo en entorno de desarrollo PC...")
    while hilo_flask.is_alive():
        time.sleep(1)