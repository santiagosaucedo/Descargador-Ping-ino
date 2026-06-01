import sys
import os
import threading
import time

# 1. Inyectar la ruta del motor móvil
ruta_raiz = os.path.dirname(os.path.abspath(__file__))
ruta_motor_movil = os.path.join(ruta_raiz, 'motor-mobile-android')
if ruta_motor_movil not in sys.path:
    sys.path.insert(0, ruta_motor_movil)

# 2. Levantar Flask en segundo plano
def iniciar_servidor_flask():
    try:
        import android_server
    except Exception as e:
        with open(os.path.join(ruta_raiz, 'error_flask.txt'), 'w') as f:
            f.write(str(e))

hilo_flask = threading.Thread(target=iniciar_servidor_flask)
hilo_flask.daemon = True
hilo_flask.start()

# 3. Levantar la App de Kivy invisible para que Android no mate el proceso
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

class PinguinoApp(App):
    def build(self):
        # Programamos la carga del WebView nativo 1 segundo después del inicio
        Clock.schedule_once(self.abrir_webview, 1.0)
        return Widget() # Retorna un contenedor vacío (el WebView se va a poner encima)

    def abrir_webview(self, dt):
        try:
            from jnius import autoclass
            from android.runnable import Runnable

            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')

            class CrearWebView(Runnable):
                def run(self):
                    activity = PythonActivity.mActivity
                    webview = WebView(activity)
                    webview.getSettings().setJavaScriptEnabled(True)
                    webview.setWebViewClient(WebViewClient())
                    # Cargamos tu backend local
                    webview.loadUrl('http://127.0.0.1:5000')
                    activity.setContentView(webview)

            CrearWebView()()
        except Exception as e:
            with open(os.path.join(ruta_raiz, 'error_webview.txt'), 'w') as f:
                f.write(str(e))

if __name__ == "__main__":
    # Arranca el bucle de Android oficial
    PinguinoApp().run()