# NetDrop

NetDrop es una aplicacion web local para compartir archivos dentro de la misma red. Puedes ejecutarla en tu computadora y acceder desde otro dispositivo usando el navegador.

Con NetDrop puedes:

- subir archivos desde el navegador;
- ver y descargar archivos compartidos;
- eliminar archivos desde la interfaz;
- generar un codigo QR para abrir la pagina mas rapido desde el celular.

## Requisitos

- Python 3.11 o superior.
- `pip` para instalar dependencias.
- Una red local compartida si quieres acceder desde otro dispositivo.

## Instalacion

1. Clona o descarga el repositorio.
2. Abre una terminal dentro de la carpeta del proyecto.
3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## 📦 Descarga para Windows (Ejecutable e Instalador de 1 Clic)

Puedes descargar la versión compilada para Windows directamente desde [GitHub Releases](https://github.com/NioyDev/NetDrop/releases):

- 💻 **`NetDrop-Setup-v2.1.0.exe`**: Instalador clásico para Windows (crea acceso directo en Escritorio y Menú Inicio).
- ⚡ **`NetDrop-Windows-Portable.exe`**: Ejecutable portable de 1 solo clic (sin necesidad de instalación ni Python).
- 📦 **`NetDrop-Windows-x64.zip`**: Archivo comprimido con la distribución ejecutable.

## Ejecutar desde el codigo fuente

En Windows:

```bash
python app.py
```

En Linux o macOS:

```bash
python3 app.py
```

Al iniciar, NetDrop:

- abre el navegador automaticamente;
- levanta un servidor local en `http://0.0.0.0:5000`;
- genera el QR de acceso en la carpeta de datos de la aplicacion.

## Uso rapido

1. Ejecuta la aplicacion.
2. Abre la interfaz en el navegador.
3. Sube los archivos que quieras compartir.
4. Desde otro dispositivo, entra usando la IP local de la computadora anfitriona y el puerto `5000`.
5. Descarga, visualiza o elimina archivos desde la web.

## Carpetas de trabajo

NetDrop guarda sus archivos en el perfil del usuario, no dentro del proyecto:

- Subidas: `%LOCALAPPDATA%\NetDrop\File`
- QR: `%LOCALAPPDATA%\NetDrop\QR`

Si ejecutas desde otras plataformas, estas carpetas se crean en el directorio de usuario correspondiente.

## Notas

- La aplicacion esta pensada para red local.
- Si no puedes entrar desde otro equipo, revisa el firewall y permite el puerto `5000`.
- La funcion de desbloqueo de archivos solo funciona en Windows.
- El acceso directo al archivo usa nombres sanitizados por seguridad.

## Tecnologias

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript, Jinja2
- QR: `qrcode`, `Pillow`

## Autor

- [Nioy](https://github.com/NioyJadelkaFp/)

## Licencia

Este proyecto se distribuye como software source-available bajo la licencia **PolyForm Noncommercial 1.0.0**.
