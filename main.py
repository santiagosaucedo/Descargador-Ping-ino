import sys
import os
import threading
import time

# 1. Inyectar la ruta del motor móvil
ruta_raiz = os.path.dirname(os.path.abspath(__file__))
ruta_motor_movil = os.path.join(ruta_raiz, 'motor-mobile-android')
if ruta_motor_movil not in sys.path:
    sys.path.insert(0, ruta_motor_movil)

# 2. Intentar buscar una ruta pública de Android para escribir el log
# Si no la encuentra (como en PC), usa la raíz del proyecto
ruta_log_publico = ruta_raiz
if 'ANDROID_ARGUMENT' in os.environ:
    # En Android, esto nos da una ruta externa segura y visible para el usuario
    from android.storage import primary_external_storage_path
    ruta_log_publico = primary_external_storage_path()

def guardar_error_en_celu(nombre_archivo, contenido_error):
    try:
        import traceback
        error_completo = traceback.format_exc()
        # Intentamos guardarlo en el almacenamiento general del celu
        path_final = os.path.join(ruta_log_publico, nombre_archivo)
        with open(path_final, 'w') as f:
            f.write(f"Error: {contenido_error}\n\nTraceback:\n{error_completo}")
    except:
        pass

# 3. Levantar Flask en segundo plano con captura de errores
def iniciar_servidor_flask():
    try:
        import android_server
    except Exception as e:
        guardar_error_en_celu('error_flask_publico.txt', str(e))

hilo_flask = threading.Thread(target=iniciar_servidor_flask)
hilo_flask.daemon = True
hilo_flask.start()

# 4. Levantar la App de Kivy invisible
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

class PinguinoApp(App):
    def build(self):
        Clock.schedule_once(self.abrir_webview, 1.0)
        return Widget()

    def abrir_webview(self, dt):
        try:
            from jnius import autoclass
            from android.runnable import Runnable

            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')

            class CrearWebView(Runnable):
                def run(self):
                    try:
                        activity = PythonActivity.mActivity
                        webview = WebView(activity)
                        webview.getSettings().setJavaScriptEnabled(True)
                        webview.setWebViewClient(WebViewClient())
                        webview.loadUrl('http://127.0.0.1:5000')
                        activity.setContentView(webview)
                    except Exception as ex:
                        guardar_error_en_celu('error_webview_inner.txt', str(ex))

            CrearWebView()()
        except Exception as e:
            guardar_error_en_celu('error_webview_publico.txt', str(e))

if __name__ == "__main__":
    try:
        PinguinoApp().run()
    except Exception as e:
        guardar_error_en_celu('error_kivy_main.txt', str(e))