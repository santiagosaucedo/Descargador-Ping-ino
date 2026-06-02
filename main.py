# 🐧 main.py (Ubicado en la raíz del proyecto)
import sys
import os
import threading

# 1. Inyectamos la ruta de tu backend móvil
ruta_raiz = os.path.dirname(os.path.abspath(__file__))
ruta_motor_movil = os.path.join(ruta_raiz, 'motor-mobile-android')
if ruta_motor_movil not in sys.path:
    sys.path.insert(0, ruta_motor_movil)

# 2. Configuración segura de almacenamiento
try:
    from android.storage import primary_external_storage_path
    ruta_descargas = os.path.join(primary_external_storage_path(), 'Download')
except ImportError:
    ruta_descargas = os.path.join(ruta_raiz, 'downloads')

os.makedirs(ruta_descargas, exist_ok=True)
os.environ['RUTA_DESCARGAS_PINGUINO'] = ruta_descargas

# 3. Lanzamos Flask en un hilo Daemon (en la sombra)
def iniciar_servidor_flask():
    try:
        import android_server
    except Exception as e:
        print(f"Error interno de Flask: {e}")

hilo_flask = threading.Thread(target=iniciar_servidor_flask)
hilo_flask.daemon = True
hilo_flask.start()

# 4. LA INTERFAZ NATIVA (ACÁ ESTÁ LA MAGIA QUE EVITA EL CRASHEO)
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

# Importamos el delegado del Hilo Principal de Android
try:
    from android.runnable import run_on_ui_thread
    from jnius import autoclass
except ImportError:
    # Fallback por si corrés el código en Windows para testear
    def run_on_ui_thread(func):
        return func

class PinguinoApp(App):
    def build(self):
        # Le damos a Flask 1.5 segundos para que asiente el servidor local antes de abrir la pantalla
        Clock.schedule_once(self.lanzar_webview_seguro, 1.5)
        return Widget()

    # 🚨 ESTA ETIQUETA ES LA QUE SALVA LA APP DEL CIERRE: Obliga a Java a correrlo en su UI Thread
    @run_on_ui_thread
    def lanzar_webview_seguro(self, dt=None):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')

            activity = PythonActivity.mActivity
            webview = WebView(activity)
            
            # Habilitamos JS y el almacenamiento DOM (Clave para que ande el "fetch" moderno en Android)
            webview.getSettings().setJavaScriptEnabled(True)
            webview.getSettings().setDomStorageEnabled(True) 
            webview.setWebViewClient(WebViewClient())
            
            # Cargamos el motor de Flask
            webview.loadUrl('http://127.0.0.1:5000')
            activity.setContentView(webview)
        except Exception as e:
            print(f"Fallo al inyectar WebView: {e}")

if __name__ == "__main__":
    PinguinoApp().run()