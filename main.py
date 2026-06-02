# 🐧 main.py (Ubicado en la raíz del proyecto)
import sys
import os
import traceback
import threading
import time
import urllib.request
import webbrowser

# --- ESCUDO GLOBAL ---
ERROR_GLOBAL = None

try:
    # 1. Configuración de dependencias base
    ruta_raiz = os.path.dirname(os.path.abspath(__file__))
    ruta_motor_movil = os.path.join(ruta_raiz, 'motor-mobile-android')
    if ruta_motor_movil not in sys.path:
        sys.path.insert(0, ruta_motor_movil)

    ES_ANDROID = 'ANDROID_ARGUMENT' in os.environ

    # 2. Hilo de Flask (Se mantiene igual)
    def iniciar_servidor_flask():
        try:
            import android_server
            android_server.app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
        except Exception as e:
            print(f"Error interno de Flask: {e}")

    # 3. Importaciones de Kivy y Android
    from kivy.app import App
    from kivy.uix.widget import Widget
    from kivy.clock import Clock
    
    if ES_ANDROID:
        from android.runnable import run_on_ui_thread
        from jnius import autoclass
        # 🚨 LIBRERÍA OFICIAL DE PERMISOS
        from android.permissions import request_permissions, Permission
    else:
        def run_on_ui_thread(func): return func

except Exception as e:
    ERROR_GLOBAL = traceback.format_exc()


# --- DEFINICIÓN DE LA APLICACIÓN ---
if ERROR_GLOBAL is None:
    class PinguinoApp(App):
        def build(self):
            if ES_ANDROID:
                # 1. PEDIMOS EL PERMISO DE FRENTE AL USUARIO CON UN POPUP
                request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
                
                # 2. Seteamos la ruta oficial de Descargas de Android
                # (No usamos os.makedirs porque la carpeta Download ya existe siempre por defecto)
                from android.storage import primary_external_storage_path
                ruta_descargas = os.path.join(primary_external_storage_path(), 'Download')
            else:
                ruta_descargas = os.path.join(ruta_raiz, 'downloads')
                os.makedirs(ruta_descargas, exist_ok=True)
            
            # 3. Le pasamos la ruta segura al backend
            os.environ['RUTA_DESCARGAS_PINGUINO'] = ruta_descargas
            
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
            if not ES_ANDROID:
                webbrowser.open('http://127.0.0.1:5000')
                return
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
                print(f"Error crítico en WebView: {e}")

else:
    # Pantalla roja de diagnóstico por si algo más falla
    from kivy.app import App
    from kivy.uix.label import Label
    from kivy.core.window import Window
    
    class PinguinoApp(App):
        def build(self):
            Window.clearcolor = (0.5, 0.1, 0.1, 1)
            lbl = Label(
                text=f"CRASH DETECTADO:\n\n{ERROR_GLOBAL}",
                font_size='11sp',
                valign='top',
                halign='left'
            )
            lbl.bind(size=lbl.setter('text_size'))
            return lbl


if __name__ == "__main__":
    if ERROR_GLOBAL is None:
        hilo_flask = threading.Thread(target=iniciar_servidor_flask)
        hilo_flask.daemon = True
        hilo_flask.start()

    PinguinoApp().run()