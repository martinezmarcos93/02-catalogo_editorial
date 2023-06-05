import sys
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, \
    QDialog, QGridLayout, QLineEdit, QPushButton, QMessageBox, QHeaderView

conn = sqlite3.connect("ventas.db")
cursor = conn.cursor()

# Crear la tabla "ventas" si no existe
cursor.execute("CREATE TABLE IF NOT EXISTS ventas (Fecha TEXT, Cliente TEXT, Tienda TEXT, Evento TEXT, Libro TEXT, Cantidad INTEGER, 'Importe Unitario' REAL, Total REAL)")

conn.commit()
conn.close()


class VentasWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editorial Thelema - Ventas")
        self.setWindowIcon(QIcon("logo3.png"))

        # Logo de la empresa
        self.logo_label = QLabel(self)
        logo_pixmap = QPixmap("logo2.png")
        logo_pixmap = logo_pixmap.scaledToWidth(200)  # Ajustar el ancho de la imagen al valor deseado
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)

        # Ajustar el tamaño de la ventana
        self.resize(800, 600)

        # Botones
        self.add_button = QPushButton("Registrar Venta", self)
        self.add_button.clicked.connect(self.open_add_dialog)

        # Planilla Excel
        self.table = QTableWidget(self)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["Fecha", "Cliente", "Tienda", "Evento", "Libro", "Cantidad", "Importe Unitario", "Total"])

        # Cargar datos desde la base de datos
        self.load_data()

        # Ajustar el tamaño de las columnas según el contenido
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Configurar la alineación del texto en las celdas de la tabla
        self.configure_table()

        # Diseño de la interfaz
        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)
        layout.addWidget(self.add_button)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def configure_table(self):
        # Alinear el texto del encabezado al centro
        for i in range(self.table.columnCount()):
            self.table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignCenter)

        # Alinear el texto de las celdas al centro
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                item = self.table.item(i, j)
                item.setTextAlignment(Qt.AlignCenter)

    def load_data(self):
        # Conexión a la base de datos
        conn = sqlite3.connect("ventas.db")
        cursor = conn.cursor()

        # Obtener los datos de las ventas
        cursor.execute("SELECT * FROM ventas")
        ventas = cursor.fetchall()

        # Cargar los datos en la tabla
        self.table.setRowCount(len(ventas))
        for i, venta in enumerate(ventas):
            for j, value in enumerate(venta):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

        # Cerrar la conexión a la base de datos
        conn.close()

    def open_add_dialog(self):
        dialog = AddVentaDialog(self)
        if dialog.exec_():
            self.load_data()


class AddVentaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Venta")

        self.fecha_edit = QLineEdit(self)
        self.cliente_edit = QLineEdit(self)
        self.tienda_edit = QLineEdit(self)
        self.evento_edit = QLineEdit(self)
        self.libro_edit = QLineEdit(self)
        self.cantidad_edit = QLineEdit(self)
        self.importe_edit = QLineEdit(self)
        self.total_edit = QLineEdit(self)
        self.total_edit.setReadOnly(True)

        self.calculate_button = QPushButton("Calcular", self)
        self.calculate_button.clicked.connect(self.calculate_total)

        self.add_button = QPushButton("Registrar", self)
        self.add_button.clicked.connect(self.add_venta)

        layout = QGridLayout()
        layout.addWidget(QLabel("Fecha:"), 0, 0)
        layout.addWidget(self.fecha_edit, 0, 1)
        layout.addWidget(QLabel("Cliente:"), 1, 0)
        layout.addWidget(self.cliente_edit, 1, 1)
        layout.addWidget(QLabel("Tienda:"), 2, 0)
        layout.addWidget(self.tienda_edit, 2, 1)
        layout.addWidget(QLabel("Evento:"), 3, 0)
        layout.addWidget(self.evento_edit, 3, 1)
        layout.addWidget(QLabel("Libro:"), 4, 0)
        layout.addWidget(self.libro_edit, 4, 1)
        layout.addWidget(QLabel("Cantidad:"), 5, 0)
        layout.addWidget(self.cantidad_edit, 5, 1)
        layout.addWidget(QLabel("Importe Unitario:"), 6, 0)
        layout.addWidget(self.importe_edit, 6, 1)
        layout.addWidget(QLabel("Total:"), 7, 0)
        layout.addWidget(self.total_edit, 7, 1)
        layout.addWidget(self.calculate_button, 8, 0, 1, 2)
        layout.addWidget(self.add_button, 9, 0, 1, 2)

        self.setLayout(layout)

    def calculate_total(self):
        cantidad = self.cantidad_edit.text()
        importe = self.importe_edit.text()
        try:
            cantidad = int(cantidad)
            importe = float(importe)
            total = cantidad * importe
            self.total_edit.setText(str(total))
        except ValueError:
            QMessageBox.warning(self, "Error", "Ingrese valores numéricos válidos para Cantidad e Importe Unitario")

    def add_venta(self):
        fecha = self.fecha_edit.text()
        cliente = self.cliente_edit.text()
        tienda = self.tienda_edit.text()
        evento = self.evento_edit.text()
        libro = self.libro_edit.text()
        cantidad = self.cantidad_edit.text()
        importe = self.importe_edit.text()
        total = self.total_edit.text()

        try:
            cantidad = int(cantidad)
            importe = float(importe)
            total = float(total)

            # Conexión a la base de datos
            conn = sqlite3.connect("ventas.db")
            cursor = conn.cursor()

            # Insertar la venta en la tabla
            cursor.execute("INSERT INTO ventas VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (fecha, cliente, tienda, evento, libro, cantidad, importe, total))

            # Cerrar la conexión a la base de datos
            conn.commit()
            conn.close()

            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Error", "Ingrese valores numéricos válidos para Cantidad, Importe Unitario y Total")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VentasWindow()
    window.show()
    sys.exit(app.exec_())
