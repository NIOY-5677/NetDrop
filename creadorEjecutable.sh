# Ejecutable para Linux
pyinstaller --onefile --windowed --add-data "templates:templates" --add-data "static:static" --icon=logo.png app.py

# Ejecutable para Windows
pyinstaller --onefile --windowed --add-data "templates;templates" --add-data "static;static" --icon=logo.ico app.py