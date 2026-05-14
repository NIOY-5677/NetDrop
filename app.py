from flask import Flask, redirect, render_template, send_file, request, jsonify
from Funciones import Qr_Generator
from Funciones import Show_File as Show_File
from Funciones.paths import ensure_runtime_dirs, qr_path, static_dir, templates_dir
import os
from werkzeug.utils import secure_filename
import secrets
import urllib.request
import sys
import threading

# Funciones propias
from Funciones.ip import sacar_ip
from Funciones.configuracion import ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from Funciones.abrirNavegador import abrir_navegador
from Funciones.close import esta_cerrado

#Lanzador
from Lanzador.main import Iniciador

app = Flask(__name__, template_folder=templates_dir(), static_folder=static_dir())
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Carpeta de destino en static/File
Files_Carpet = os.path.join(app.static_folder, 'Files')
if not os.path.exists(Files_Carpet):
    os.makedirs(Files_Carpet)

def allowed_file(filename):
    """Permite archivos con extensiones válidas o archivos sin extensión (opcional)."""
    if '.' not in filename:
        return True # Permitimos archivos sin extensión por si son binarios de Linux
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- RUTAS ---

@app.route('/')
def index():
    File = Show_File.Show_File()
    return render_template('index.html', File=File)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'UPFile' not in request.files:
            return redirect('/update')

        f = request.files.get('UPFile')
        if not f or f.filename == '':
            return redirect('/update')

        filename = secure_filename(f.filename)

        if allowed_file(filename):
            file_path = os.path.join(Files_Carpet, filename)
            try:
                f.save(file_path)
                return redirect('/')
            except Exception as e:
                return redirect('/update')
        else:
            print(f"🚫 Extensión no permitida: {filename}")
            return redirect('/update')
    return redirect('/')

@app.route('/descarga/<filename>', methods=['GET'])
def descarga(filename):
    filename = secure_filename(filename)
    file_path = os.path.join(Files_Carpet, filename)
    
    if not os.path.exists(file_path):
        return redirect('/')
    
    try:
        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception as e:
        print(f"Error al descargar {filename}: {e}")
        return redirect('/')

@app.route('/eliminar/<filename>', methods=['POST', 'GET'])
def eliminar(filename):
    filename = secure_filename(filename)
    file_path = os.path.join(Files_Carpet, filename)
    
    if not os.path.exists(file_path):
        return redirect('/')
    
    try:
        os.remove(file_path)
        print(f"✓ Archivo eliminado: {filename}")
    except Exception as e:
        print(f"Error al eliminar {filename}: {e}")
    
    return redirect('/')

@app.route('/update')
def update():
    return render_template('Up_Data.html')

@app.route('/qrgenerator')
def QR_Generador_Vista():
    return render_template('Qr_Generator.html')

@app.route('/qr-image')
def qr_image():
    if not os.path.exists(qr_path()):
        Qr_Generator.Generar_QR()
    return send_file(qr_path())

@app.route('/qr')
def qr():
    Qr_Generator.Generar_QR()
    return redirect('/qrgenerator')


# ... Tus otras importaciones y funciones (esta_cerrado, Qr_Generator, etc.)

def ejecutar_servidor():
    """Función para correr Flask en un hilo secundario."""
    # IMPORTANTE: use_reloader=False es vital para que la UI no se abra dos veces
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)

if __name__ == '__main__':
    if esta_cerrado():
        # Escenario 1: El servidor está apagado. Arrancamos ambos.
        if not os.environ.get('WERKZEUG_RUN_MAIN'):
            print(f"🚀 Iniciando NetDrop en: http://{sacar_ip()}:5000")
            Qr_Generator.Generar_QR()
            # abrir_navegador() # Podés comentarlo si la UI ya muestra la app
        
        # 1. Creamos y lanzamos el hilo del servidor
        servidor_thread = threading.Thread(target=ejecutar_servidor)
        servidor_thread.daemon = True # Para que se apague al cerrar la ventana
        servidor_thread.start()

        # 2. Arrancamos la interfaz de PySide6 en el hilo principal
        # Asegurate de que Iniciador() ejecute app.exec() al final
        Iniciador() 

    else:
        # Escenario 2: Ya está corriendo. Solo avisamos y abrimos pestaña.
        print("\n" + "="*40)
        print("⚠️  NETDROP YA ESTÁ EN EJECUCIÓN")
        print(f"🔗 Abriendo pestaña en: http://{sacar_ip()}:5000")
        print("="*40 + "\n")
        
        abrir_navegador()
        sys.exit()