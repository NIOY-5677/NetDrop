@echo off
title NetDrop - Compilador para Windows
echo =========================================================
echo       COMPILADOR DE NETDROP PARA WINDOWS (.EXE & SETUP)
echo =========================================================
echo.

echo [1/4] Instalando dependencias necesarias...
pip install -r requirements.txt
pip install pyinstaller pywebview

echo.
echo [2/4] Compilando ejecutable Portable (OneFile)...
pyinstaller --clean distribucion\NetDrop-Windows-OneFile.spec

echo.
echo [3/4] Compilando distribucion para Instalador (Folder)...
pyinstaller --clean distribucion\NetDrop-Windows-Folder.spec

echo.
echo [4/4] Buscando Inno Setup para crear el instalador Setup...
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" distribucion\NetDrop-Setup.iss
    echo [✓] Instalador generado exitosamente en dist\NetDrop-Setup-v2.1.0.exe
) else (
    echo [!] Inno Setup 6 no esta instalado en C:\Program Files (x86)\Inno Setup 6.
    echo [!] Solo se generaron los ejecutables en dist\ NetDrop-Windows-Portable.exe y dist\NetDrop-Windows
)

echo.
echo =========================================================
echo COMPILACION COMPLETADA!
echo.
echo Archivos generados en la carpeta 'dist':
echo  - NetDrop-Windows-Portable.exe  (Ejecutable standalone)
echo  - NetDrop-Setup-v2.1.0.exe       (Instalador Setup facil)
echo =========================================================
pause
