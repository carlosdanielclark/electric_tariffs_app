from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from pathlib import Path


class LoginView(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Electric Tariffs App")
        self.setFixedSize(800, 600)
        self.setStyleSheet(self.load_stylesheet())
        self.setup_ui()

    def load_stylesheet(self) -> str:
        return """
        QDialog {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e0f7fa, stop:1 #b2ebf2);
        }
        QLabel#welcome {
            font-size: 28px;
            font-weight: bold;
            color: #333333;
            margin-top: 20px;
        }
        QLineEdit {
            padding: 12px;
            font-size: 16px;
            border: 1px solid #999999;
            border-radius: 8px;
            background: white;
            color: #333333;               /* ✅ Texto visible */
            selection-background-color: #00C8D6;
            selection-color: white;
        }
        QPushButton {
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            color: white;
            background-color: #00C8D6;
            border: none;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: #00a5b3;
        }
        QWidget#form_container {
            background-color: white;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        """

    def setup_ui(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Icono de la app
        icon_path = Path("assets") / "app_icon.png"
        if icon_path.exists():
            icon_label = QLabel()
            pixmap = QPixmap(str(icon_path)).scaled(
                80, 80,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(icon_label)

        welcome_label = QLabel("Bienvenido")
        welcome_label.setObjectName("welcome")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(welcome_label)

        # Formulario
        form_container = QWidget()
        form_container.setObjectName("form_container")
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(15)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.setStyleSheet("color: #333333;")  # Fallback

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("color: #333333;")  # Fallback

        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.accept)

        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.login_button)

        main_layout.addWidget(form_container)
        self.setLayout(main_layout)