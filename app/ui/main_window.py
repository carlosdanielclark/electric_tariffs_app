from __future__ import annotations
from typing import Any
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFrame
from app.ui.login_window import LoginWindow
from app.ui.dashboard_view import DashboardView
from app.ui.reading_form import ReadingForm
from app.ui.config_view import ConfigView
from app.infrastructure.logger.activity_logger import ActivityLogger
from app.domain.entities.user import User

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Electric Tariffs App")
        self.resize(1000, 640)
        self.current_user = None
        self.logger = ActivityLogger()
        self.setup_ui()

    def setup_ui(self) -> None:
        central = QWidget()
        main_layout = QHBoxLayout()

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sb_layout = QVBoxLayout()
        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_register = QPushButton("Registrar lectura")
        self.btn_config = QPushButton("Configuración")
        self.btn_logout = QPushButton("Cerrar sesión")
        for b in (self.btn_dashboard, self.btn_register, self.btn_config, self.btn_logout):
            sb_layout.addWidget(b)
        sb_layout.addStretch()
        sidebar.setLayout(sb_layout)

        self.content_frame = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_frame.setLayout(self.content_layout)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_frame, stretch=1)
        central.setLayout(main_layout)
        self.setCentralWidget(central)

        self.btn_dashboard.clicked.connect(self.show_dashboard)
        self.btn_register.clicked.connect(self.show_register)
        self.btn_config.clicked.connect(self.show_config)
        self.btn_logout.clicked.connect(self.logout)

        self.show_login()

    def clear_content(self) -> None:
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

    def show_login(self) -> None:
        self.clear_content()
        login = LoginWindow(on_login_callback=self.on_login_success)
        self.content_layout.addWidget(login)
        self.set_sidebar_enabled(False)

    def on_login_success(self, user: User) -> None:
        self.current_user = user
        self.logger.log_event(user.id, "login", f"Usuario {user.username} inició sesión")
        self.set_sidebar_enabled(True)
        self.show_dashboard()

    def set_sidebar_enabled(self, enabled: bool) -> None:
        for btn in (self.btn_dashboard, self.btn_register, self.btn_config, self.btn_logout):
            btn.setEnabled(enabled)

    def show_dashboard(self) -> None:
        if self.current_user is None:
            return
        self.clear_content()
        view = DashboardView(current_user=self.current_user)
        self.content_layout.addWidget(view)

    def show_register(self) -> None:
        if self.current_user is None:
            return
        self.clear_content()
        form = ReadingForm(current_user=self.current_user)
        self.content_layout.addWidget(form)

    def show_config(self) -> None:
        self.clear_content()
        cfg = ConfigView()
        self.content_layout.addWidget(cfg)

    def logout(self) -> None:
        if self.current_user:
            self.logger.log_event(self.current_user.id, "logout", f"Usuario {self.current_user.username} cerró sesión")
        self.current_user = None
        self.show_login()