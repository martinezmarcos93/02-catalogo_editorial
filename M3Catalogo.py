import sys
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, \
    QDialog, QGridLayout, QLineEdit, QMessageBox, QHBoxLayout, QHeaderView

conn = sqlite3.connect("catalogo.db")
cursor = conn.cursor()

# Crear la tabla "libros" si no existe
cursor.execute("CREATE TABLE IF NOT EXISTS libros (Libro TEXT, Autor TEXT, Año INTEGER, ISBN TEXT, 'Versión Digital' TEXT, 'En Imprenta' TEXT, Ejemplares INTEGER, 'En Stock' INTEGER)")

conn.commit()
conn.close()


class CatalogWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editorial Thelema - Catálogo")
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
        self.add_button = QPushButton("Añadir", self)
        self.add_button.clicked.connect(self.open_add_dialog)

        self.edit_button = QPushButton("Modificar", self)
        self.edit_button.clicked.connect(self.open_edit_dialog)

        # Planilla Excel
        self.table = QTableWidget(self)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["Libro", "Autor", "Año", "ISBN", "Versión Digital", "En Imprenta", "Ejemplares", "En Stock"])

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
        layout.addWidget(self.edit_button)
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
        conn = sqlite3.connect("catalogo.db")
        cursor = conn.cursor()

        # Obtener los datos del catálogo
        cursor.execute("SELECT * FROM libros")
        libros = cursor.fetchall()

        # Cargar los datos en la tabla
        self.table.setRowCount(len(libros))
        for i, libro in enumerate(libros):
            for j, value in enumerate(libro):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

        # Cerrar la conexión a la base de datos
        conn.close()

    def open_add_dialog(self):
        dialog = AddDialog(self)
        if dialog.exec_():
            self.load_data()

    def open_edit_dialog(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            dialog = EditDialog(self, selected_row)
            if dialog.exec_():
                self.load_data()


class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Añadir Libro")

        # Campos de entrada
        self.libro_edit = QLineEdit()
        self.autor_edit = QLineEdit()
        self.ano_edit = QLineEdit()
        self.isbn_edit = QLineEdit()
        self.version_edit = QLineEdit()
        self.imprenta_edit = QLineEdit()
        self.ejemplares_edit = QLineEdit()
        self.stock_edit = QLineEdit()

        # Botones
        self.add_button = QPushButton("Añadir", self)
        self.add_button.clicked.connect(self.add_book)
        self.cancel_button = QPushButton("Cancelar", self)
        self.cancel_button.clicked.connect(self.reject)

        # Diseño de la interfaz
        layout = QGridLayout()
        layout.addWidget(QLabel("Libro:"), 0, 0)
        layout.addWidget(self.libro_edit, 0, 1)
        layout.addWidget(QLabel("Autor:"), 1, 0)
        layout.addWidget(self.autor_edit, 1, 1)
        layout.addWidget(QLabel("Año:"), 2, 0)
        layout.addWidget(self.ano_edit, 2, 1)
        layout.addWidget(QLabel("ISBN:"), 3, 0)
        layout.addWidget(self.isbn_edit, 3, 1)
        layout.addWidget(QLabel("Versión Digital:"), 4, 0)
        layout.addWidget(self.version_edit, 4, 1)
        layout.addWidget(QLabel("En Imprenta:"), 5, 0)
        layout.addWidget(self.imprenta_edit, 5, 1)
        layout.addWidget(QLabel("Ejemplares:"), 6, 0)
        layout.addWidget(self.ejemplares_edit, 6, 1)
        layout.addWidget(QLabel("En Stock:"), 7, 0)
        layout.addWidget(self.stock_edit, 7, 1)
        layout.addWidget(self.add_button, 8, 0)
        layout.addWidget(self.cancel_button, 8, 1)
        self.setLayout(layout)

    def add_book(self):
        libro = self.libro_edit.text()
        autor = self.autor_edit.text()
        ano = self.ano_edit.text()
        isbn = self.isbn_edit.text()
        version = self.version_edit.text()
        imprenta = self.imprenta_edit.text()
        ejemplares = self.ejemplares_edit.text()
        stock = self.stock_edit.text()

        # Conexión a la base de datos
        conn = sqlite3.connect("catalogo.db")
        cursor = conn.cursor()

        # Insertar el libro en la base de datos
        cursor.execute("INSERT INTO libros (Libro, Autor, Año, ISBN, 'Versión Digital', 'En Imprenta', Ejemplares, 'En Stock') VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (libro, autor, ano, isbn, version, imprenta, ejemplares, stock))

        # Confirmar los cambios y cerrar la conexión a la base de datos
        conn.commit()
        conn.close()

        self.accept()


class EditDialog(QDialog):
    def __init__(self, parent=None, row=-1):
        super().__init__(parent)
        self.setWindowTitle("Modificar Libro")

        self.row = row

        # Campos de entrada
        self.libro_edit = QLineEdit()
        self.autor_edit = QLineEdit()
        self.ano_edit = QLineEdit()
        self.isbn_edit = QLineEdit()
        self.version_edit = QLineEdit()
        self.imprenta_edit = QLineEdit()
        self.ejemplares_edit = QLineEdit()
        self.stock_edit = QLineEdit()

        # Botones
        self.update_button = QPushButton("Actualizar", self)
        self.update_button.clicked.connect(self.update_book)
        self.cancel_button = QPushButton("Cancelar", self)
        self.cancel_button.clicked.connect(self.reject)

        # Diseño de la interfaz
        layout = QGridLayout()
        layout.addWidget(QLabel("Libro:"), 0, 0)
        layout.addWidget(self.libro_edit, 0, 1)
        layout.addWidget(QLabel("Autor:"), 1, 0)
        layout.addWidget(self.autor_edit, 1, 1)
        layout.addWidget(QLabel("Año:"), 2, 0)
        layout.addWidget(self.ano_edit, 2, 1)
        layout.addWidget(QLabel("ISBN:"), 3, 0)
        layout.addWidget(self.isbn_edit, 3, 1)
        layout.addWidget(QLabel("Versión Digital:"), 4, 0)
        layout.addWidget(self.version_edit, 4, 1)
        layout.addWidget(QLabel("En Imprenta:"), 5, 0)
        layout.addWidget(self.imprenta_edit, 5, 1)
        layout.addWidget(QLabel("Ejemplares:"), 6, 0)
        layout.addWidget(self.ejemplares_edit, 6, 1)
        layout.addWidget(QLabel("En Stock:"), 7, 0)
        layout.addWidget(self.stock_edit, 7, 1)
        layout.addWidget(self.update_button, 8, 0)
        layout.addWidget(self.cancel_button, 8, 1)
        self.setLayout(layout)

        # Cargar los datos del libro seleccionado
        self.load_book_data()

    def load_book_data(self):
        # Conexión a la base de datos
        conn = sqlite3.connect("catalogo.db")
        cursor = conn.cursor()

        # Obtener los datos del libro seleccionado
        cursor.execute("SELECT * FROM libros WHERE rowid=?", (self.row + 1,))
        libro = cursor.fetchone()

        # Cargar los datos en los campos de entrada
        self.libro_edit.setText(libro[0])
        self.autor_edit.setText(libro[1])
        self.ano_edit.setText(str(libro[2]))
        self.isbn_edit.setText(libro[3])
        self.version_edit.setText(libro[4])
        self.imprenta_edit.setText(libro[5])
        self.ejemplares_edit.setText(str(libro[6]))
        self.stock_edit.setText(str(libro[7]))

        # Cerrar la conexión a la base de datos
        conn.close()

    def update_book(self):
        libro = self.libro_edit.text()
        autor = self.autor_edit.text()
        ano = self.ano_edit.text()
        isbn = self.isbn_edit.text()
        version = self.version_edit.text()
        imprenta = self.imprenta_edit.text()
        ejemplares = self.ejemplares_edit.text()
        stock = self.stock_edit.text()

        # Conexión a la base de datos
        conn = sqlite3.connect("catalogo.db")
        cursor = conn.cursor()

        # Actualizar el libro en la base de datos
        cursor.execute("UPDATE libros SET Libro=?, Autor=?, Año=?, ISBN=?, 'Versión Digital'=?, 'En Imprenta'=?, Ejemplares=?, 'En Stock'=? WHERE rowid=?",
                       (libro, autor, ano, isbn, version, imprenta, ejemplares, stock, self.row + 1))

        # Confirmar los cambios y cerrar la conexión a la base de datos
        conn.commit()
        conn.close()

        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    catalog_window = CatalogWindow()
    catalog_window.show()
    sys.exit(app.exec())
