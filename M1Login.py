import sys
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QCheckBox, QDialog
from PyQt5.QtCore import QTimer
from M2VentanaPrincipal import WorkWindow
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont


class SuccessfulLoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión Exitoso")
        self.setWindowIcon(QIcon("logo3.png"))

        label = QLabel("¡Inicio de sesión exitoso!")
        font = QFont()
        font.setPointSize(16)  # Tamaño de fuente personalizado
        label.setFont(font)

        accept_button = QPushButton("Aceptar")
        accept_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(accept_button)
        self.setLayout(layout)

class LoginWindow(QWidget):
    login_successful = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editorial Thelema - Inicio de Sesión")
        self.setWindowIcon(QIcon("logo3.png"))  # Establecer la imagen como icono de la ventana
        
        # Logo de la empresa
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(QPixmap("logo2.png").scaledToWidth(400))  # Ajustar el ancho de la imagen al valor deseado
        self.logo_label.setScaledContents(True)  # Ajustar el tamaño de la imagen automáticamente
        
        # Campos de entrada de usuario y contraseña
        self.username_label = QLabel("Usuario:")
        self.username_edit = QLineEdit()
        self.password_label = QLabel("Contraseña:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        
        # Botón de inicio de sesión
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.login)  # Conectar el botón a la función de inicio de sesión
        
        # Checkbox para recordar contraseña
        self.remember_checkbox = QCheckBox("Recordar contraseña")
        
        # Diseño de la interfaz
        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.remember_checkbox)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

        self.load_remembered_password()  # Cargar los datos recordados

    def login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        # Verificar el usuario y contraseña
        if username == "editorialthelema" and password == "thelemita":
            if self.remember_checkbox.isChecked():
                self.remember_password(username, password)
            self.show_successful_login_dialog()  # Mostrar el diálogo de inicio de sesión exitoso
        else:
            QMessageBox.warning(self, "Inicio de Sesión", "Usuario o contraseña incorrectos.")
    
    def remember_password(self, username, password):
        # Guardar el usuario y contraseña en un archivo
        with open("credenciales.txt", "w") as file:
            file.write(f"{username}\n{password}")

    def load_remembered_password(self):
        # Cargar el usuario y contraseña recordados desde el archivo
        try:
            with open("credenciales.txt", "r") as file:
                lines = file.readlines()
                username = lines[0].strip()
                password = lines[1].strip()
                self.username_edit.setText(username)
                self.password_edit.setText(password)
                self.remember_checkbox.setChecked(True)
        except FileNotFoundError:
            pass
    
    def show_successful_login_dialog(self):
        dialog = SuccessfulLoginDialog()
        dialog.accepted.connect(self.open_work_window)  # Conectar la señal de aceptar el diálogo a la función de abrir la ventana de trabajo
        dialog.exec_()
    
    def open_work_window(self):
        self.work_window = WorkWindow()
        self.work_window.show()
        self.close()  # Cerrar la ventana de inicio de sesión

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    
    login_window.login_successful.connect(login_window.show_successful_login_dialog)  # Conectar la señal de inicio de sesión exitoso a la función de mostrar el diálogo
    
    login_window.show()
    sys.exit(app.exec_())
