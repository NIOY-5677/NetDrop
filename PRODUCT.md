# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Usuarios en red local (hogar, oficina, grupos de trabajo) que necesitan enviar y recibir archivos de forma rápida y privada entre la computadora principal y cualquier otro dispositivo conectado (móviles, tablets, otras laptops).

## Product Purpose

Servidor web local sin conexión a internet que facilita la transferencia de archivos en tiempo real mediante un navegador web, ofreciendo código QR de escaneo rápido y gestión directa (subir, ver, descargar, eliminar).

## Positioning

Solución ligera y privada de transferencia local en un clic, que no requiere servidores externos ni instalación de aplicaciones en los dispositivos receptores.

## Operating Context

Entorno de red local (Wi-Fi / LAN), ejecutado en `http://0.0.0.0:5000`. Acceso desde dispositivos móviles o exploradores secundarios.

## Capabilities and Constraints

- Subida multi-archivo desde la interfaz web.
- Generación automática de código QR con la IP local para fácil vinculación con móviles.
- Visualización previa, descarga y eliminación de archivos compartidos.
- Almacenamiento seguro aislado en la carpeta de usuario del sistema.
- Backend en Python Flask con plantillas Jinja2 y frontend estándar.

## Brand Commitments

- Nombre: NetDrop
- Autor: Nioy
- Enfoque: Interfaz limpia, rápida, funcional y directa.

## Evidence on Hand

- Código backend funcional en `app.py`.
- Plantillas HTML e interfaz CSS en `templates/` y `static/`.
- Repositorio y documentación existente en `README.md`.

## Product Principles

1. **Privacidad y Velocidad Local:** Cero dependencia de servicios en la nube.
2. **Acceso Inmediato:** Escaneo QR o IP directa sin registro ni configuración pesada.
3. **Simplicidad Impecable:** Interfaz moderna, clara e intuitiva sin saturación visual.
