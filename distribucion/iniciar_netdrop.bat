@echo off
title NetDrop - Compartir Archivos en Red Local
echo ===================================================
echo               INICIANDO NETDROP (WINDOWS)
echo ===================================================
echo.
echo Comprobando Python en el sistema...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python no esta instalado o no esta en el PATH.
    echo [!] Por favor instala Python o ejecuta el instalador NetDrop-Setup.exe
    pause
    exit /b
)

echo Instalando dependencias necesarias...
pip install -r requirements.txt

echo.
echo Arrancando NetDrop...
python app.py
pause
