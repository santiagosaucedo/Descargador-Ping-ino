# 🐧 main.py (Ubicado en la raíz del proyecto)
import sys
import os
import threading
import time
import urllib.request
import webbrowser

# 1. Configuración de rutas
ruta_raiz = os.path.dirname(os.path.abspath(__file__))
ruta_motor_movil = os.path.join(ruta_raiz, 'motor-mobile-android')
if ruta_motor_movil not in sys.path:
    sys.path.insert(0, ruta_motor_movil)

ES_ANDROID = 'ANDROID_ARGUMENT' in os.environ

if ES_ANDROID:
    try:
        from android.storage import primary_external_storage_path
        ruta_descargas = os.path.join(primary_external_storage_path(), 'Download')
    except ImportError:
        ruta_descargas = os.path.join(ruta_raiz, 'downloads')
else:
    ruta_descargas = os.path.join(ruta_raiz, 'downloads')

os.makedirs(ruta_descargas, exist_ok=True)
os.environ['RUTA_DESCARGAS_PINGUINO'] = ruta_descargas

# 2. Hilo de Flask (¡Acá estaba el bug!)
def iniciar_servidor_flask():
    try:
        import android_server
        print("Iniciando motor Flask en segundo plano...")
        # AHORA SÍ LE DAMOS LA ORDEN DE ARRANCAR
        android_server.app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Error interno de Flask: {e}")

# 3. MOCKING: Intentamos importar Kivy
try:
    from kivy.app import App
    from kivy.uix.widget import Widget
    from kivy.clock import Clock
    try:
        from android.runnable import run_on_ui_thread
        from jnius import autoclass
    except ImportError:
        def run_on_ui_thread(func): return func
    KIVY_DISPONIBLE = True
except ImportError:
    KIVY_DISPONIBLE = False

# 4. Definición de la App Nativa para Android
if KIVY_DISPONIBLE:
    class PinguinoApp(App):
        def build(self):
            Clock.schedule_interval(self.esperar_servidor, 0.5)
            return Widget()

        def esperar_servidor(self, dt):
            try:
                if urllib.request.urlopen("http://127.0.0.1:5000/").getcode() == 200:
                    Clock.unschedule(self.esperar_servidor)
                    self.lanzar_interfaz()
            except Exception:
                pass

        @run_on_ui_thread
        def lanzar_interfaz(self):
            try:
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                WebView = autoclass('android.webkit.WebView')
                WebViewClient = autoclass('android.webkit.WebViewClient')
                
                activity = PythonActivity.mActivity
                webview = WebView(activity)
                webview.getSettings().setJavaScriptEnabled(True)
                webview.getSettings().setDomStorageEnabled(True) 
                webview.setWebViewClient(WebViewClient())
                webview.loadUrl('http://127.0.0.1:5000')
                activity.setContentView(webview)
            except Exception as e:
                print(f"Error crítico en Java WebView: {e}")

# 5. Punto de Entrada Dinámico
if __name__ == "__main__":
    hilo_flask = threading.Thread(target=iniciar_servidor_flask)
    hilo_flask.daemon = True
    hilo_flask.start()

    if KIVY_DISPONIBLE:
        PinguinoApp().run()
    else:
        print("Kivy no detectado. Iniciando en Modo Test de Escritorio...")
        servidor_arriba = False
        
        for _ in range(10):
            try:
                if urllib.request.urlopen("http://127.0.0.1:5000/").getcode() == 200:
                    servidor_arriba = True
                    break
            except Exception:
                time.sleep(0.5)
        
        if servidor_arriba:
            print("¡Flask detectado! Abriendo el navegador del sistema...")
            webbrowser.open('http://127.0.0.1:5000')
            while True:
                time.sleep(1)
        else:
            print("Error: Flask no arrancó correctamente.")