from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QStackedWidget, QLabel, QFrame
)
from PyQt6.QtCore import Qt
from .dashboard_view import DashboardView
from .history_view import HistoryView
from .graph_view import GraphView
from .user_stats_view import UserStatsView
from ..widgets.reading_form_widget import ReadingFormWidget


class MainWindow(QMainWindow):
    def __init__(self, user, reading_service, user_service) -> None:
        super().__init__()
        self.user = user
        self.reading_service = reading_service
        self.user_service = user_service
        self.setWindowTitle(f"Electric Tariffs App - {user.username}")
        self.setMinimumSize(1000, 700)
        self.setup_ui()

    def setup_ui(self) -> None:
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar, 1)

        self.stacked_widget = QStackedWidget()
        self.dashboard_view = DashboardView(self.user.id, self.reading_service)
        self.history_view = HistoryView(self.user.id, self.reading_service)
        self.graph_view = GraphView(self.user.id, self.reading_service)

        self.stacked_widget.addWidget(self.dashboard_view)
        self.stacked_widget.addWidget(self.history_view)
        self.stacked_widget.addWidget(self.graph_view)

        if self.user.rol == "admin":
            self.user_stats_view = UserStatsView(self.user_service)
            self.stacked_widget.addWidget(self.user_stats_view)

        main_layout.addWidget(self.stacked_widget, 4)
        self.setCentralWidget(central_widget)

        self.dashboard_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.history_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.graph_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        if self.user.rol == "admin":
            self.stats_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

        self.update_reading_form()

    def create_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setStyleSheet("""
            background-color: #333333;
            color: white;
            font-family: sans-serif;
        """)
        layout = QVBoxLayout(sidebar)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 30, 20, 20)

        title = QLabel("Menú")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        self.dashboard_btn = self.create_menu_button("Dashboard")
        self.history_btn = self.create_menu_button("Historial de lectura")
        self.graph_btn = self.create_menu_button("Gráfica")
        layout.addWidget(self.dashboard_btn)
        layout.addWidget(self.history_btn)
        layout.addWidget(self.graph_btn)

        if self.user.rol == "admin":
            self.stats_btn = self.create_menu_button("Estadísticas de usuarios")
            layout.addWidget(self.stats_btn)

        layout.addSpacing(30)
        layout.addWidget(QLabel("Registrar lectura", styleSheet="font-weight: bold;"))

        self.reading_form = ReadingFormWidget()
        self.reading_form.reading_submitted.connect(self.handle_reading_submission)
        layout.addWidget(self.reading_form)
        layout.addStretch()

        logout_btn = QPushButton("Cerrar sesión")
        logout_btn.setStyleSheet("""
            background-color: #00C8D6;
            color: white;
            padding: 8px;
            border-radius: 6px;
            font-weight: bold;
        """)
        logout_btn.clicked.connect(self.close)
        layout.addWidget(logout_btn)

        return sidebar

    def create_menu_button(self, text: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setStyleSheet("""
            text-align: left;
            padding: 10px;
            border-radius: 6px;
            font-size: 14px;
        """)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return btn

    def update_reading_form(self) -> None:
        last = self.reading_service.get_last_reading_by_user(self.user.id)
        prev = float(last.lectura_actual) if last else 0.0
        self.reading_form.previous_input.setText(f"{prev:.2f}")

    def handle_reading_submission(self, previous: float, current: float) -> None:
        try:
            self.reading_service.register_reading(
                user_id=self.user.id,
                lectura_actual=current,
                lectura_anterior=previous
            )
            self.update_reading_form()
            self.dashboard_view.load_data()
            self.history_view.load_data()
            self.graph_view.load_data()
        except Exception:
            pass