from __future__ import annotations
from typing import Callable, Any
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from app.application.services.auth_service import AuthService
from app.infrastructure.repositories.sqlite_user_repository import SQLiteUserRepository


class LoginWindow(QWidget):
    def __init__(self, on_login_callback: Callable[[Any], None], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.on_login = on_login_callback
        self.repo = SQLiteUserRepository()
        self.auth = AuthService(self.repo)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.setWindowTitle("Login - Electric Tariffs")
        layout = QVBoxLayout()
        title = QLabel("Bienvenido")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Usuario")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Contraseña")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        btn_layout = QHBoxLayout()
        login_btn = QPushButton("Iniciar sesión")
        register_btn = QPushButton("Registrar usuario")
        login_btn.clicked.connect(self.try_login)
        register_btn.clicked.connect(self.try_register)
        btn_layout.addWidget(login_btn)
        btn_layout.addWidget(register_btn)

        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.setFixedWidth(320)

    def try_login(self) -> None:
        username = self.username.text().strip()
        password = self.password.text().strip()
        user = self.auth.authenticate(username, password)
        if user:
            self.on_login(user)
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")

    def try_register(self) -> None:
        username = self.username.text().strip()
        password = self.password.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Completa usuario y contraseña para registrar.")
            return
        try:
            self.auth.create_user(name=username, username=username, password=password, role="usuario")
            QMessageBox.information(self, "Registrado", f"Usuario {username} registrado correctamente.")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))