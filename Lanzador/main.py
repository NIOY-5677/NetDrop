import sys
import os
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon  # Necesario para el icono
from Funciones.abrirNavegador import abrir_navegador

class MiApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NetDrop Desktop")
        # Bloqueamos el tamaño para que no se pueda estirar
        self.setFixedSize(350, 250)

        self.ruta_base = os.path.dirname(os.path.abspath(__file__))
        self.establecer_icono()

        self.btn_web = QPushButton("Abrir NetDrop")
        self.btn_salir = QPushButton("Cerrar NetDrop")

        self.btn_web.setObjectName("btn_abrir")
        self.btn_salir.setObjectName("btn_cerrar")

        self.btn_web.clicked.connect(abrir_navegador)
        self.btn_salir.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40) 
        layout.addWidget(self.btn_web)
        layout.addWidget(self.btn_salir)
        self.setLayout(layout)

        self.cargar_estilos()

    def establecer_icono(self):
        """Busca el archivo logo.png en la carpeta del script."""
        ruta_icono = os.path.join(self.ruta_base, "../static/Logo/logo-sin-fondo.png")
        if os.path.exists(ruta_icono):
            self.setWindowIcon(QIcon(ruta_icono))

    def cargar_estilos(self):
        """Carga el archivo QSS y lo aplica."""
        ruta_qss = os.path.join(self.ruta_base, "estilos.qss")
        if os.path.exists(ruta_qss):
            with open(ruta_qss, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        else:
            print(f"⚠️ Alerta: No se encontró {ruta_qss}")

def Iniciador():
    app = QApplication(sys.argv)
    ventana = MiApp()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    Iniciador()