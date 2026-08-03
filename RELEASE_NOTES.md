# NetDrop v2.0.0 - Rediseño Editorial, Temas JSON & Sincronización en Tiempo Real

¡Nos alegra presentar **NetDrop v2.0.0**! Esta versión incluye una reconstrucción estética completa, un motor de temas en tiempo real basado en JSON, sincronización instantánea entre dispositivos y optimizaciones masivas de memoria.

---

### 🎨 1. Sistema Dinámico de Temas basado en JSON (con 5 Temas Predeterminados)
- **Personalización total por JSON:** Crea, edita o importa cualquier paleta de colores mediante estructuras `.json`.
- **5 Temas listos para usar:** *Cálido Terracota* (predeterminado), *Oscuro Minimal*, *Bosque Verde*, *Noche Ámbar* y *Nórdico Frío*.
- **Panel de Ajustes (⚙️):** Vista previa visual de cada tema, descarga de plantillas JSON e importador de archivos directo.
- **Persistencia en disco:** Guardado permanente en `.active_theme.json` compatible con la app de escritorio y navegadores móviles.

### ⚡ 2. Sincronización en Tiempo Real entre Dispositivos (Live Sync)
- **Sondeo inteligente cada 2 segundos:** Cualquier archivo subido desde una computadora o teléfono aparece de inmediato en todos los demás dispositivos conectados sin necesidad de recargar la página.

### 🖼️ 3. Vista Previa Instantánea de Archivos (Live Preview)
- **Lightbox integrado:** Visualización en vivo para imágenes (`JPG`, `PNG`, `GIF`, `WEBP`, `SVG`), videos (`MP4`, `WEBM`, `MOV`), audio (`MP3`, `WAV`, `FLAC`) y código/texto (`PY`, `JS`, `HTML`, `CSS`, `JSON`, `MD`).

### 📱 4. Optimización de Memoria RAM para Móviles (Zero Mobile OOM Crashes)
- Subida de archivos por fragmentos de **2MB** con liberación activa de memoria en Javascript y límites en la RAM de Flask para transferencias fluidas de archivos pesados desde celulares.

### ✨ 5. Rediseño Estilo Tarjeta Editorial Humana (High-Craft UX)
- Lista de archivos estructurada en tarjetas elevadas con iconos SVG diferenciados por tipo, metadatos calculados en **KB/MB/GB** y botones de acción rápida de 1 clic (**Ver**, **Copiar Enlace**, **Descargar**, **Eliminar**).

### 🔔 6. Notificaciones Toast Inteligentes con Multiplicador
- Agrupación automática de acciones repetidas con contador visual animado (`x1`, `x2`, `x5`...) y diseño adaptativo a cada tema.

---

### 🛠️ Archivos de Instalación y Ejecutables Incluidos:
- `NetDrop-Linux-x64`: Ejecutable binario nativo independiente para Linux (64-bit).
- `netdrop-installer.deb`: Paquete de instalación para Debian, Ubuntu, Linux Mint y derivados.
- `NetDrop-Windows-x64.zip`: Paquete con lanzador de 1-clic (`iniciar_netdrop.bat`) e instalador de dependencias automático para Windows.
