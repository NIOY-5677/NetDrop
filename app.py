from flask import Flask, jsonify, redirect, render_template, request, send_file, send_from_directory
from Funciones import Qr_Generator
from Funciones import Show_File as Show_File
from Funciones.paths import ensure_runtime_dirs, qr_path, static_dir, templates_dir
import os
import shutil
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
import secrets
import urllib.request
import sys
import threading
import webview
import time

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
app.config['MAX_FORM_MEMORY_SIZE'] = 10 * 1024 * 1024  # 10MB máx en RAM por petición

# Carpeta de destino persistente para archivos subidos.
Files_Carpet, _ = ensure_runtime_dirs()
Partial_Carpet = os.path.join(Files_Carpet, ".partials")
os.makedirs(Partial_Carpet, exist_ok=True)

def allowed_file(filename):
    """Permite archivos con extensiones válidas o archivos sin extensión (opcional)."""
    if '.' not in filename:
        return True # Permitimos archivos sin extensión por si son binarios de Linux
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def guardar_archivo_subido(file_storage, file_path):
    """Guarda copiando en bloques para evitar picos de memoria con subidas grandes."""
    with open(file_path, "wb") as destino:
        shutil.copyfileobj(file_storage.stream, destino, length=1024 * 1024)

def cert_paths():
    base = os.path.dirname(os.path.abspath(__file__))
    cert = os.path.join(base, 'cert.crt')
    key = os.path.join(base, 'cert.key')
    return cert, key

def es_https():
    cert, key = cert_paths()
    return os.path.exists(cert) and os.path.exists(key)

# --- RUTAS ---

@app.route('/')
def index():
    File = Show_File.Show_File()
    ip_local = sacar_ip()
    protocolo = 'https' if es_https() else 'http'
    return render_template('index.html', File=File, ip_local=ip_local, protocolo=protocolo)

@app.route('/settings')
def settings():
    ip_local = sacar_ip()
    protocolo = 'https' if es_https() else 'http'
    return render_template('settings.html', ip_local=ip_local, protocolo=protocolo)

@app.route('/api/sync-status')
def sync_status():
    files = Show_File.Show_File()
    count = len(files)
    latest_mtime = 0
    if os.path.exists(Files_Carpet):
        for f in os.listdir(Files_Carpet):
            fp = os.path.join(Files_Carpet, f)
            if os.path.isfile(fp):
                mtime = os.path.getmtime(fp)
                if mtime > latest_mtime:
                    latest_mtime = mtime
    return jsonify({
        "ok": True,
        "count": count,
        "latest_mtime": latest_mtime
    })

THEME_FILE_PATH = os.path.join(Files_Carpet, ".active_theme.json")

@app.route('/api/theme', methods=['GET', 'POST'])
def api_theme():
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            if data:
                with open(THEME_FILE_PATH, 'w', encoding='utf-8') as f:
                    import json
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return jsonify({"ok": True})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 400
    
    if os.path.exists(THEME_FILE_PATH):
        try:
            with open(THEME_FILE_PATH, 'r', encoding='utf-8') as f:
                import json
                theme_data = json.load(f)
                return jsonify({"ok": True, "theme": theme_data})
        except Exception:
            pass
    return jsonify({"ok": True, "theme": None})

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'UPFile' not in request.files:
            return redirect('/update')

        f = request.files.get('UPFile')
        if not f or f.filename == '':
            return redirect('/update')

        filename = secure_filename(f.filename)
        if not filename:
            print("🚫 Nombre de archivo inválido")
            return redirect('/update')

        if allowed_file(filename):
            file_path = os.path.join(Files_Carpet, filename)
            try:
                guardar_archivo_subido(f, file_path)
                return redirect('/')
            except Exception as e:
                print(f"Error al subir {filename}: {e}")
                return redirect('/update')
        else:
            print(f"🚫 Extensión no permitida: {filename}")
            return redirect('/update')
    return redirect('/')

@app.errorhandler(RequestEntityTooLarge)
def archivo_demasiado_grande(error):
    print(f"🚫 Archivo demasiado grande. Límite: {MAX_FILE_SIZE} bytes")
    return redirect('/update')

@app.route('/upload-chunk', methods=['POST'])
def upload_chunk():
    chunk_field = 'file_chunk' if 'file_chunk' in request.files else 'UPFile'
    if chunk_field not in request.files:
        return jsonify({"ok": False, "error": "No llegó el archivo"}), 400

    original_name = request.form.get('filename', '')
    filename = secure_filename(original_name)
    if not filename:
        return jsonify({"ok": False, "error": "Nombre de archivo inválido"}), 400

    if not allowed_file(filename):
        return jsonify({"ok": False, "error": f"Extensión no permitida: {filename}"}), 400

    try:
        chunk_index = int(request.form.get('chunk_index', '0'))
        total_chunks = int(request.form.get('total_chunks', '1'))
        total_size = int(request.form.get('total_size', '0'))
    except ValueError:
        return jsonify({"ok": False, "error": "Datos de subida inválidos"}), 400

    if total_size and total_size > MAX_FILE_SIZE:
        return jsonify({"ok": False, "error": "El archivo supera el límite permitido"}), 413

    upload_id = secure_filename(request.form.get('upload_id', ''))
    if not upload_id:
        return jsonify({"ok": False, "error": "Subida inválida"}), 400

    chunk = request.files[chunk_field]
    partial_path = os.path.join(Partial_Carpet, f"{upload_id}.part")
    final_path = os.path.join(Files_Carpet, filename)

    try:
        if chunk_index == 0 and os.path.exists(partial_path):
            os.remove(partial_path)

        with open(partial_path, "ab") as destino:
            shutil.copyfileobj(chunk.stream, destino, length=1024 * 1024)

        if chunk_index + 1 == total_chunks:
            if os.path.getsize(partial_path) > MAX_FILE_SIZE:
                os.remove(partial_path)
                return jsonify({"ok": False, "error": "El archivo supera el límite permitido"}), 413

            os.replace(partial_path, final_path)
            print(f"✓ Archivo subido desde chunks: {filename}")
            return jsonify({"ok": True, "complete": True})

        return jsonify({"ok": True, "complete": False})
    except Exception as e:
        print(f"Error al subir chunk de {filename}: {e}")
        return jsonify({"ok": False, "error": "No se pudo guardar el archivo"}), 500

@app.route('/archivo/<path:filename>', methods=['GET'])
def archivo(filename):
    filename = secure_filename(filename)
    return send_from_directory(Files_Carpet, filename)

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

def ejecutar_servidor():
    """Función para correr Flask en el hilo secundario (con soporte SSL/HTTPS si existen certificados)."""
    cert, key = cert_paths()
    if os.path.exists(cert) and os.path.exists(key):
        print("🔒 Servidor seguro HTTPS activado con certificados SSL")
        app.run(debug=True, host="0.0.0.0", port=5000, ssl_context=(cert, key), use_reloader=False)
    else:
        app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)

def arrancar_webview():
    """Función para correr la interfaz ligera nativa en el hilo principal."""
    time.sleep(0.8) 
    proto = 'https' if es_https() else 'http'
    webview.create_window(
        title='NetDrop Desktop', 
        url=f'{proto}://127.0.0.1:5000',
        width=850,
        height=650,
        min_size=(850, 650),
        resizable=True
    )
    webview.start()

if __name__ == '__main__':
    if esta_cerrado():
        # Escenario 1: El servidor está apagado. Arrancamos de cero.
        if not os.environ.get('WERKZEUG_RUN_MAIN'):
            print(f"🚀 Iniciando NetDrop en: http://{sacar_ip()}:5000")
            Qr_Generator.Generar_QR()
        
        # 1. Lanzamos el servidor Flask en segundo plano
        servidor_thread = threading.Thread(target=ejecutar_servidor)
        servidor_thread.daemon = True 
        servidor_thread.start()

        # 2. Levantamos el WebView ligero en el hilo principal
        arrancar_webview()

    else:
        # Escenario 2: Ya hay una instancia de NetDrop abierta.
        print("\n" + "="*40)
        print("⚠️  NETDROP YA ESTÁ EN EJECUCIÓN")
        print(f"🔗 Abriendo pestaña en: http://{sacar_ip()}:5000")
        print("="*40 + "\n")
        
        abrir_navegador() 
        sys.exit()
