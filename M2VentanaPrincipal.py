import sys
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from M3Catalogo import CatalogWindow, AddDialog, EditDialog
from M4Ventas import VentasWindow, AddVentaDialog


class WorkWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editorial Thelema - Ventana de trabajo")
        self.setWindowIcon(QIcon("logo3.png"))  # Establecer la imagen como icono de la ventana

        # Logo de la empresa
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(QPixmap("logo2.png"))  # Utilizar el tamaño original de la imagen
        self.logo_label.setScaledContents(True)  # Ajustar el tamaño de la imagen automáticamente
        
        # Ajustar el tamaño de la ventana
        self.resize(400, 300)  # Ancho: 400 píxeles, Altura: 300 píxeles
        self.adjust_logo_size()  # Ajustar el tamaño del logo

        # Botones
        self.catalog_button = QPushButton("Catálogo", self)
        self.catalog_button.clicked.connect(self.open_catalog)

        self.sales_button = QPushButton("Ventas", self)
        self.sales_button.clicked.connect(self.open_sales)

        # Diseño de la interfaz
        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)
        layout.addWidget(self.catalog_button)
        layout.addWidget(self.sales_button)
        self.setLayout(layout)

    def adjust_logo_size(self):
        window_width = self.width()
        logo_width = self.logo_label.pixmap().width()
        if logo_width > window_width:
            scaled_logo = self.logo_label.pixmap().scaledToWidth(window_width)
            self.logo_label.setPixmap(scaled_logo)

    def resizeEvent(self, event):
        self.adjust_logo_size()
        super().resizeEvent(event)

    def open_catalog(self):
        self.catalogo = CatalogWindow()
        self.catalogo.show()

    def open_sales(self):
        self.ventas = VentasWindow()
        self.ventas.show()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    work_window = WorkWindow()
    work_window.show()
    sys.exit(app.exec_())
