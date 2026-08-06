# -*- mode: python ; coding: utf-8 -*-

import os
import sys

block_cipher = None

a = Analysis(
    ['../app.py'],
    pathex=['..'],
    binaries=[],
    datas=[
        ('../templates', 'templates'),
        ('../static', 'static')
    ],
    hiddenimports=[
        'flask',
        'werkzeug',
        'webview',
        'qrcode',
        'PIL',
        'engineio.async_drivers.threading',
        'jinja2',
        'Lanzador',
        'Lanzador.main',
        'Funciones',
        'Funciones.ip',
        'Funciones.abrirNavegador',
        'Funciones.close',
        'Funciones.paths',
        'Funciones.configuracion',
        'Funciones.Qr_Generator',
        'Funciones.Show_File'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5', 'tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NetDrop-Windows-Portable',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../static/Logo/Logo.ico',
)
