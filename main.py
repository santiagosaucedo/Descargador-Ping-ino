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

# 2. CONFIGURACIÓN DE RUTAS DE ALMACENAMIENTO
if 'ANDROID_ARGUMENT' in os.environ:
    from android.storage import app_storage_dir
    ruta_descargas = os.environ.get('RUTA_DESCARGAS_PINGUINO', '/sdcard/Download')
else:
    ruta_descargas = os.path.join(ruta_raiz, 'downloads')

os.makedirs(ruta_descargas, exist_ok=True)
os.environ['RUTA_DESCARGAS_PINGUINO'] = ruta_descargas

# 3. Lanzamos Flask en un hilo independiente para no congelar la pantalla de Android
def iniciar_servidor_flask():
    try:
        import android_server
    except Exception as e:
        print(f"Error al levantar Flask: {e}")

hilo_flask = threading.Thread(target=iniciar_servidor_flask)
hilo_flask.daemon = True
hilo_flask.start()

# 4. LEVANTAMOS LA INTERFAZ COMPATIBLE CON SDL2
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

class PinguinoApp(App):
    def build(self):
        # Esperamos 1 segundo a que Flask se asiente y disparamos el WebView
        Clock.schedule_once(self.abrir_webview, 1.0)
        return Widget() # Retorna un contenedor limpio

    def abrir_webview(self, dt):
        # Levantamos el navegador nativo mediante Pyjnius (Java Bridge)
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
                    # Forzamos a que maneje las alertas y la escala de forma nativa
                    webview.setWebViewClient(WebViewClient())
                    # Apuntamos a tu Flask local
                    webview.loadUrl('http://127.0.0.1:5000')
                    activity.setContentView(webview)

            CrearWebView()()
        except Exception as e:
            print(f"Fallo al inyectar WebView de Java: {e}")

if __name__ == "__main__":
    PinguinoApp().run()