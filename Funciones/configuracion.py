# --- CONFIGURACIÓN ---
# Ampliamos para soportar instaladores y archivos de sistema
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp', 'heic', 'heif',
    'mp4', 'mp3', 'wav', 'aac',
    'avi', 'mov', 'zip', 'rar', '7z', 'tar', 'gz', 'py', 'js', 'html', 'css', 
    'java', 'm4a', 'opus', 'apk', 'exe', 'msi', 'json'
}
MAX_FILE_SIZE = 1000 * 1024 * 1024  # 1GB
