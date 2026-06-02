# 🐧 main.py (Ubicado en la raíz del proyecto)
import sys
import os
import threading
import time
import webbrowser

# 1. Configuración de Rutas base
ruta_raiz = os.path.dirname(os.path.abspath(__file__))
ruta_motor_movil = os.path.join(ruta_raiz, 'motor-mobile-android')
if ruta_motor_movil not in sys.path:
    sys.path.insert(0, ruta_motor_movil)

ES_ANDROID = 'ANDROID_ARGUMENT' in os.environ

if ES_ANDROID:
    # Ruta pública legal de Android (No requiere pedir permisos para crear archivos aquí)
    ruta_descargas = '/storage/emulated/0/Download/Pinguino'
else:
    ruta_descargas = os.path.join(ruta_raiz, 'downloads')

os.environ['RUTA_DESCARGAS_PINGUINO'] = ruta_descargas

# 2. Importaciones Híbridas
try:
    from kivy.app import App
    from kivy.uix.widget import Widget
    KIVY_DISPONIBLE = True
except ImportError:
    KIVY_DISPONIBLE = False

if ES_ANDROID:
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
else:
    def run_on_ui_thread(func): return func

# 3. El Orquestador de Arranque (Totalmente aislado del hilo gráfico)
def orquestador_segundo_plano(app_kivy):
    try:
        import android_server
        # Levantamos Flask
        threading.Thread(
            target=lambda: android_server.app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False), 
            daemon=True
        ).start()
        
        # Le damos 2 segundos exactos a Flask para asentar el puerto SIN CONGELAR el celular
        time.sleep(2.0)
        
        # Le ordenamos al celular que inyecte la pantalla
        if KIVY_DISPONIBLE and ES_ANDROID:
            app_kivy.lanzar_interfaz()
        elif not ES_ANDROID:
            webbrowser.open('http://127.0.0.1:5000')
    except Exception as e:
        print(f"Error crítico en el backend: {e}")

# 4. Contenedor de Interfaz
if KIVY_DISPONIBLE:
    class PinguinoApp(App):
        def build(self):
            # Iniciamos la carga de Flask en la sombra mientras Kivy pinta un fondo neutro
            threading.Thread(target=orquestador_segundo_plano, args=(self,), daemon=True).start()
            return Widget()

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
                print(f"Fallo nativo de Java: {e}")

if __name__ == "__main__":
    if KIVY_DISPONIBLE:
        PinguinoApp().run()
    else:
        orquestador_segundo_plano(None)
        while True: time.sleep(1)