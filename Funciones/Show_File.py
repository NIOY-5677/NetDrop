import os
from datetime import datetime
from urllib.parse import quote

from Funciones.paths import upload_dir


def formatear_tamano(tamano):
    for unidad in ['B', 'KB', 'MB', 'GB', 'TB']:
        if tamano < 1024.0:
            return f"{tamano:.1f} {unidad}".replace('.0 ', ' ')
        tamano /= 1024.0
    return f"{tamano:.1f} PB"


def Show_File():
    Ruta = upload_dir()
    archivos = []

    if os.path.exists(Ruta):
        lista_archivos = sorted(os.listdir(Ruta), key=lambda x: os.path.getmtime(os.path.join(Ruta, x)), reverse=True)

        for nombre_archivo in lista_archivos:
            if nombre_archivo.startswith('.'):
                continue
            ruta_completa = os.path.join(Ruta, nombre_archivo)

            if os.path.isfile(ruta_completa):
                timestamp = os.path.getmtime(ruta_completa)
                fecha_legible = datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M')
                tamano_bytes = os.path.getsize(ruta_completa)
                tamano_legible = formatear_tamano(tamano_bytes)

                archivos.append({
                    "nombre": nombre_archivo,
                    "ruta": f"/archivo/{quote(nombre_archivo)}",
                    "tipo": nombre_archivo.split(".")[-1].lower() if '.' in nombre_archivo else '',
                    "fecha": fecha_legible,
                    "tamano_bytes": tamano_bytes,
                    "tamano_legible": tamano_legible
                })
    return archivos
